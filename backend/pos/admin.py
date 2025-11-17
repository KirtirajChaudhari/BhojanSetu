from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import MenuItem, MenuCategory, Order, OrderItem

User = get_user_model()


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_vegetarian', 'is_available')
    list_filter = ('category', 'is_vegetarian', 'is_vegan', 'is_available', 'spice_level')
    list_editable = ('is_available',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest_name', 'table_number', 'waiter', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
