from django.contrib import admin
from .models import Cart, MyOrder, OrderItem

admin.site.register(Cart)
admin.site.register(MyOrder)
admin.site.register(OrderItem)

# class OderItemAdmin(admin.ModelAdmin):
#     list_display=('id','quantity','order_time','ordered')
