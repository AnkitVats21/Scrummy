# accounts.admin.py

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, UserProfile, OTP, Food, Restaurent, FoodSearch

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin','otp')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('active','otp','admin','staff','restaurent')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    inlines = (UserProfileInline, )


admin.site.register(User, UserAdmin)

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('otp_email','otp')


@admin.register(Restaurent)
class RestaurentAdmin(admin.ModelAdmin):
    list_display = ('restaurent_name', 'zip_code', 'restaurent_address')

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display =('name', 'category', 'rating', 'price')

admin.site.register(FoodSearch)