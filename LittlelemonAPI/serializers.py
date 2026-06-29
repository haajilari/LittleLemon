from rest_framework import serializers
from .models import MenuItem, Category
from decimal import Decimal


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']

class MenuItemSerializer(serializers.ModelSerializer):
    # stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name="calc_tax")
    category = CategorySerializer
    class Meta:
        model = MenuItem
        fields = ['id','title','price','inventory','price_after_tax','category']

    def calc_tax(self,product:MenuItem):
        return  product.price * Decimal(1.1)