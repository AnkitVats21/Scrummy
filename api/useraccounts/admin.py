from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, UserProfile, OTP, Restaurent, Food


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'Role', 'is_restaurent', 'password',)}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'Role', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'is_staff', 'Role', 'is_restaurent')
    search_fields = ('email',)
    ordering = ('email',)
    inlines = (UserProfileInline, )

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('otp_email','otp')

@admin.register(Restaurent)
class RestaurentAdmin(admin.ModelAdmin):
    list_display = ('restaurent_name', 'zip_code', 'restaurent_address')

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display =('name', 'category', 'rating', 'price')