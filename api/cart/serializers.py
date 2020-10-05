from .models import Cart, MyOrder, OrderItem, CheckoutAddress, Payment
from rest_framework import serializers

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model   = OrderItem
        fields  = ('id','user','username',
        'ordered','item',
        'item_name','quantity',
        'get_total_item_price','delivery_time')

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

# class MyOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model   = MyOrder
#         fields = ('id',)

class CheckoutAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model   = CheckoutAddress
        fields  = ('id','user','phone','address','zip')

class Payment(serializers.ModelSerializer):
    class Meta:
        model   = Payment
        field   = ('id','user','amount','timestamp')