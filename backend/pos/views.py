from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import io
from reportlab.pdfgen import canvas

from .models import MenuItem, MenuCategory, Order, User
from .serializers import MenuItemSerializer, MenuCategorySerializer, OrderSerializer, UserTinySerializer


def _has_role(user, allowed_roles):
    if not user or not getattr(user, 'is_authenticated', False):
        return False
    if user.is_superuser:
        return True
    return getattr(user, 'role', None) in allowed_roles


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login endpoint - accepts username and password, returns user data and token"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=username, password=password)
    
    if user is None:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    login(request, user)
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'email': user.email,
        },
        'token': token.key
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout endpoint - invalidates token"""
    if hasattr(request.user, 'auth_token'):
        request.user.auth_token.delete()
    logout(request)
    return Response({'message': 'Logged out successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Returns current authenticated user"""
    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'role': request.user.role,
        'email': request.user.email,
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def menu_categories(request):
    """List all menu categories"""
    categories = MenuCategory.objects.all()
    serializer = MenuCategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def menu_list(request):
    if request.method == 'GET':
        items = MenuItem.objects.filter(is_available=True).select_related('category')
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data)

    # Only staff can add menu items
    if not request.user.is_authenticated or not request.user.is_staff:
        return Response({'error': 'Staff access required'}, status=status.HTTP_403_FORBIDDEN)

    serializer = MenuItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def orders_list_create(request):
    if request.method == 'GET':
        status_q = request.query_params.get('status')
        qs = Order.objects.all().order_by('-created_at')
        if status_q:
            qs = qs.filter(status=status_q)
        serializer = OrderSerializer(qs, many=True)
        return Response(serializer.data)

    # Only waiters may create orders (or superusers)
    if not _has_role(request.user, ['waiter']):
        return Response({'detail': 'Authentication with waiter role required'}, status=status.HTTP_403_FORBIDDEN)

    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save()
        # attach waiter
        order.waiter = request.user
        order.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return Response(OrderSerializer(order).data)


@api_view(['POST'])
def order_change_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    status_val = request.data.get('status')
    if status_val not in dict(Order.STATUS_CHOICES):
        return Response({'error': 'invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    # Role-based permissions for status changes
    # reception can accept/close, chef can move to preparing/ready/served
    allowed = []
    if status_val in [Order.STATUS_ACCEPTED, Order.STATUS_CLOSED]:
        allowed = ['reception']
    elif status_val in [Order.STATUS_PREPARING, Order.STATUS_READY, Order.STATUS_SERVED]:
        allowed = ['chef']
    else:
        allowed = ['waiter', 'reception', 'chef']

    if not _has_role(request.user, allowed):
        return Response({'detail': 'Insufficient role to change to this status'}, status=status.HTTP_403_FORBIDDEN)

    order.status = status_val
    order.save()
    return Response(OrderSerializer(order).data)


@api_view(['GET', 'POST'])
def order_bill(request, pk):
    order = get_object_or_404(Order, pk=pk)
    data = OrderSerializer(order).data
    # Simple bill text
    lines = [f"Order #{order.id}", f"Guest: {order.guest_name}", f"Table: {order.table_number}", 'Items:']
    for it in data['items']:
        lines.append(f" - {it['quantity']} x {it['menu_item']['name']} @ {it['unit_price']} = {float(it['unit_price']) * it['quantity']}")
    lines.append(f"Total: {data['total']}")
    bill_text = '\n'.join(lines)

    # Generate PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    y = 800
    p.setFont('Helvetica-Bold', 16)
    p.drawString(50, y, f"Invoice - Order #{order.id}")
    y -= 40
    p.setFont('Helvetica', 12)
    for line in lines:
        p.drawString(50, y, line)
        y -= 20
        if y < 60:
            p.showPage()
            y = 800
    p.showPage()
    p.save()
    buffer.seek(0)
    pdf_data = buffer.getvalue()

    # If POST with email -> send email
    if request.method == 'POST':
        to_email = request.data.get('email')
        if to_email:
            email = EmailMessage(subject=f'Your bill for Order #{order.id}', body=bill_text, from_email=settings.DEFAULT_FROM_EMAIL, to=[to_email])
            email.attach(f'Order_{order.id}.pdf', pdf_data, 'application/pdf')
            try:
                email.send()
                return Response({'status': 'emailed', 'email': to_email})
            except Exception as e:
                return Response({'error': f'Email failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'error': 'no email provided'}, status=status.HTTP_400_BAD_REQUEST)

    # Return PDF as base64 for preview
    import base64
    pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
    return Response({'bill_text': bill_text, 'order': data, 'pdf': pdf_base64})


@api_view(['GET'])
@permission_classes([AllowAny])
def table_stats(request):
    """Get statistics about tables and orders"""
    from django.db.models import Count, Q
    
    # Get all active orders (not closed)
    active_orders = Order.objects.exclude(status='closed').select_related('waiter')
    
    # Group by table
    occupied_tables = {}
    for order in active_orders:
        table = order.table_number
        if table not in occupied_tables:
            occupied_tables[table] = []
        occupied_tables[table].append(OrderSerializer(order).data)
    
    # Calculate statistics
    total_orders = Order.objects.count()
    active_count = active_orders.count()
    closed_count = Order.objects.filter(status='closed').count()
    
    status_counts = {}
    for choice in Order.STATUS_CHOICES:
        status = choice[0]
        count = Order.objects.filter(status=status).count()
        status_counts[status] = count
    
    return Response({
        'occupied_tables': occupied_tables,
        'total_tables_occupied': len(occupied_tables),
        'total_orders': total_orders,
        'active_orders': active_count,
        'closed_orders': closed_count,
        'status_breakdown': status_counts,
    })
