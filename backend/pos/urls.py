from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/me/', views.current_user, name='current-user'),
    
    # Menu
    path('menu/categories/', views.menu_categories, name='menu-categories'),
    path('menu/', views.menu_list, name='menu-list'),
    
    # Orders
    path('orders/', views.orders_list_create, name='orders-list-create'),
    path('orders/<int:pk>/', views.order_detail, name='order-detail'),
    path('orders/<int:pk>/status/', views.order_change_status, name='order-change-status'),
    path('orders/<int:pk>/bill/', views.order_bill, name='order-bill'),
    path('tables/stats/', views.table_stats, name='table-stats'),
]
