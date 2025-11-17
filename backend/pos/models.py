from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_WAITER = 'waiter'
    ROLE_RECEPTION = 'reception'
    ROLE_CHEF = 'chef'

    ROLE_CHOICES = [
        (ROLE_WAITER, 'Waiter'),
        (ROLE_RECEPTION, 'Receptionist'),
        (ROLE_CHEF, 'Chef'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_WAITER)

    def __str__(self):
        return f"{self.username} ({self.role})"


class MenuCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Menu Categories'

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    spice_level = models.CharField(max_length=20, choices=[
        ('mild', 'Mild'),
        ('medium', 'Medium'),
        ('hot', 'Hot'),
        ('very_hot', 'Very Hot'),
    ], blank=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} (₹{self.price})"


class Order(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_PREPARING = 'preparing'
    STATUS_READY = 'ready'
    STATUS_SERVED = 'served'
    STATUS_CLOSED = 'closed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_PREPARING, 'Preparing'),
        (STATUS_READY, 'Ready'),
        (STATUS_SERVED, 'Served'),
        (STATUS_CLOSED, 'Closed'),
    ]

    guest_name = models.CharField(max_length=200)
    table_number = models.CharField(max_length=50)
    waiter = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='orders')
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum([item.total_price() for item in self.items.all()])

    def __str__(self):
        return f"Order #{self.id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.menu_item.price
        super().save(*args, **kwargs)

    def total_price(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"
