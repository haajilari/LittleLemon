from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User , Group
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,throttle_classes
from rest_framework import status
from rest_framework import viewsets 
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from .throttles import TenCallsPerMinute
# class MenuItemsView(generics.ListCreateAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer

# class SingleMenuiItemView(generics.RetrieveUpdateAPIView,generics.DestroyAPIView):
#     queryset= MenuItem.objects.all()
#     serializer_class = MenuItemSerializer



class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields=['price','inventory']
    search_fields=['title','category__title']

    def get_throttles(self):
        if self.action == 'create':
            throttle_classes = [UserRateThrottle]
        else:
            throttle_classes = []
        return [throttle() for throttle in throttle_classes]

@api_view(['GET','POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        if category_name:
            items=items.filter(category__title=category_name)
        if to_price:
            items=items.filter(price=to_price)
        if search:
            items = items.filter(title__contains=search)
        if ordering:
            ordering_fields= ordering.split(",")
            items = items.order_by(*ordering_fields)
    
        serialized_item = MenuItemSerializer(items,many=True)
        return Response(serialized_item.data)
    if request.method == 'POST':
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data,status.HTTP_201_CREATED)

@api_view(['GET','POST',"PUT","DELETE"])
def single_item (request,id):
    item=get_object_or_404(MenuItem,pk=id)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)

@api_view()
@throttle_classes([TenCallsPerMinute])
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"Message":"Some Secret Message..."})


@api_view()
@permission_classes([IsAuthenticated])
def me(request):
    return Response(request.user.email)

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name="Manager").exists():
        return Response({"message":"Only Manager Should See This"})
    else:
        return Response({"Message":"You are not authorized"},403)
    

@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"Message":"Successful"})

@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def throttle_check_auth(request):
    return Response({"Message":"Message for the logged in users only"})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']
    if username:
        user= get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        managers.user_set.add(user)
        return Response({'message':"Manager Found! :)"})
    return Response({"Message":"Manager is OK! :)"})