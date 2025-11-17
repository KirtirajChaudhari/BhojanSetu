from rest_framework import serializers
from django.conf import settings
from .models import MenuItem, MenuCategory, Order, OrderItem


class UserTinySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    role = serializers.CharField()


class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ['id', 'name', 'description', 'order']


class MenuItemSerializer(serializers.ModelSerializer):
    category = MenuCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuCategory.objects.all(), 
        write_only=True, 
        source='category'
    )

    class Meta:
        model = MenuItem
        fields = ['id', 'category', 'category_id', 'name', 'description', 'price', 
                  'is_vegetarian', 'is_vegan', 'spice_level', 'is_available']


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all(), write_only=True, source='menu_item')
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_id', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total = serializers.SerializerMethodField()
    waiter = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'guest_name', 'table_number', 'waiter', 'status', 'created_at', 'items', 'total']

    def get_total(self, obj):
        return obj.total()

    def get_waiter(self, obj):
        if obj.waiter:
            return UserTinySerializer(obj.waiter).data
        return None

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        # waiter will be set in the view (from request.user) where appropriate
        order = Order.objects.create(**validated_data)
        for item in items_data:
            menu_item = item.get('menu_item')
            quantity = item.get('quantity', 1)
            unit_price = getattr(menu_item, 'price', 0)
            OrderItem.objects.create(order=order, menu_item=menu_item, quantity=quantity, unit_price=unit_price)
        return order
