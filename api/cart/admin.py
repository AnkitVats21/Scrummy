from django.contrib import admin
from .models import Cart, MyOrder, OrderItem,CheckoutAddress,Payment

admin.site.register(Cart)
admin.site.register(MyOrder)
admin.site.register(OrderItem)
admin.site.register(CheckoutAddress)
admin.site.register(Payment)

# class OderItemAdmin(admin.ModelAdmin):
#     list_display=('id','quantity','order_time','ordered')
