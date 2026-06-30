from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # path('menu-items', views.MenuItemsView.as_view()),
    # path('menu-items/<int:pk>', views.SingleMenuiItemView.as_view()),
    # path('menu-items/', views.menu_items),
    # path('menu-items/<int:pk>', views.single_item)
    path('menu-items',views.MenuItemsViewSet.as_view({'get':'list'})),
    path('menu-items/<int:pk>',views.MenuItemsViewSet.as_view({'get':'retrieve'})),
    path('secret/',views.secret),
    path('api-token-auth/',obtain_auth_token),
    # path('throttle-check/',views.throttle_check)
    # path('throttle-chec-auth/',views.throttle_check_auth)
    path('me/', views.me),
    path('manager-view/',views.manager_view)
]