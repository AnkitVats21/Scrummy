from .models import Cart, MyOrder, OrderItem
from rest_framework import serializers

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model   = OrderItem
        fields  = ('id','username',
        'ordered','item',
        'item_name','quantity',
        'get_total_item_price')

    def create(self, validated_data):
        return OrderItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity',instance.quantity)
        instance.save()
        return instance

        
class CartSerializer(serializers.ModelSerializer):
    #items = OrderItemSerializer(required=True)
    class Meta:
        model   = Cart
        fields = ('id','user','username','items',
        'items_name','start_date',
        'ordered_date','ordered',
        'get_total_price')

class MyOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model   = MyOrder
        fields = ('id',)