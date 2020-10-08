from django.contrib import admin
from .models import Cart,  OrderItem,CheckoutAddress,Payment,MyOrder

admin.site.register(Cart)
admin.site.register(MyOrder)
admin.site.register(OrderItem)
admin.site.register(Payment)

# class OderItemAdmin(admin.ModelAdmin):
#     list_display=('id','quantity','order_time','ordered')

@admin.register(CheckoutAddress)
class CheckoutAddressAdmin(admin.ModelAdmin):
    list_display=('user','address','zip')