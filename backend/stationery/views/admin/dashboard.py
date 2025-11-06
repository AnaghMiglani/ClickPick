from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ...models import ActiveOrders, PastOrders, ActivePrintOuts, PastPrintOuts
from ...permissions import IsAdminOrStaff


class AdminGetAllActiveOrders(APIView):
    """Get all active orders from all users"""
    permission_classes = (IsAdminOrStaff, )
    
    def get(self, request):
        all_orders = ActiveOrders.objects.select_related('user', 'item').all()
        
        data = []
        for order in all_orders:
            data.append({
                'order_id': order.order_id,
                'user_id': order.user.id if order.user else None,
                'user_name': order.user.name if order.user else 'Unknown',
                'user_email': order.user.email if order.user else 'N/A',
                'item_id': order.item.id if order.item else None,
                'item_name': order.item.item if order.item else 'Unknown',
                'quantity': order.quantity,
                'cost': str(order.cost),
                'custom_message': order.custom_message,
                'order_time': order.order_time,
            })
        
        return Response(data, status=status.HTTP_200_OK)


class AdminGetAllActivePrintouts(APIView):
    """Get all active printouts from all users"""
    permission_classes = (IsAdminOrStaff, )
    
    def get(self, request):
        all_printouts = ActivePrintOuts.objects.select_related('user').all()
        
        data = []
        for printout in all_printouts:
            data.append({
                'order_id': printout.order_id,
                'user_id': printout.user.id if printout.user else None,
                'user_name': printout.user.name if printout.user else 'Unknown',
                'user_email': printout.user.email if printout.user else 'N/A',
                'coloured_pages': printout.coloured_pages,
                'black_and_white_pages': printout.black_and_white_pages,
                'print_on_one_side': printout.print_on_one_side,
                'cost': str(printout.cost),
                'custom_message': printout.custom_message,
                'order_time': printout.order_time,
                'file': request.build_absolute_uri(printout.file.url) if printout.file else None,
            })
        
        return Response(data, status=status.HTTP_200_OK)


class AdminGetAllPastOrders(APIView):
    """Get all past orders from all users"""
    permission_classes = (IsAdminOrStaff, )
    
    def get(self, request):
        all_orders = PastOrders.objects.select_related('user', 'item').all()
        
        data = []
        for order in all_orders:
            data.append({
                'order_id': order.order_id,
                'user_id': order.user.id if order.user else None,
                'user_name': order.user.name if order.user else 'Unknown',
                'user_email': order.user.email if order.user else 'N/A',
                'item_id': order.item.id if order.item else None,
                'item_name': order.item.item if order.item else 'Unknown',
                'quantity': order.quantity,
                'cost': str(order.cost),
                'custom_message': order.custom_message,
                'order_time': order.order_time,
            })
        
        return Response(data, status=status.HTTP_200_OK)


class AdminGetAllPastPrintouts(APIView):
    """Get all past printouts from all users"""
    permission_classes = (IsAdminOrStaff, )
    
    def get(self, request):
        all_printouts = PastPrintOuts.objects.select_related('user').all()
        
        data = []
        for printout in all_printouts:
            data.append({
                'order_id': printout.order_id,
                'user_id': printout.user.id if printout.user else None,
                'user_name': printout.user.name if printout.user else 'Unknown',
                'user_email': printout.user.email if printout.user else 'N/A',
                'coloured_pages': printout.coloured_pages,
                'black_and_white_pages': printout.black_and_white_pages,
                'print_on_one_side': printout.print_on_one_side,
                'cost': str(printout.cost),
                'custom_message': printout.custom_message,
                'order_time': printout.order_time,
                'file': request.build_absolute_uri(printout.file.url) if printout.file else None,
            })
        
        return Response(data, status=status.HTTP_200_OK)


class AdminDashboardStats(APIView):
    """Get dashboard statistics"""
    permission_classes = (IsAdminOrStaff, )
    
    def get(self, request):
        from django.utils import timezone
        
        today = timezone.now().date()
        
        orders_today = ActiveOrders.objects.filter(order_time__date=today)
        printouts_today = ActivePrintOuts.objects.filter(order_time__date=today)
        
        total_orders_today = orders_today.count() + printouts_today.count()
        total_revenue_today = (
            sum(float(o.cost) for o in orders_today) + 
            sum(float(p.cost) for p in printouts_today)
        )
        
        completed_orders_today = (
            PastOrders.objects.filter(order_time__date=today).count() +
            PastPrintOuts.objects.filter(order_time__date=today).count()
        )
        
        active_orders_count = ActiveOrders.objects.count()
        active_printouts_count = ActivePrintOuts.objects.count()
        
        return Response({
            'new_orders_count': total_orders_today,
            'total_revenue_today': round(total_revenue_today, 2),
            'completed_orders_count': completed_orders_today,
            'active_orders_count': active_orders_count,
            'active_printouts_count': active_printouts_count,
            'total_active_count': active_orders_count + active_printouts_count,
        }, status=status.HTTP_200_OK)


class AdminGetOrderDetails(APIView):
    """Get detailed information for a specific order"""
    permission_classes = (IsAdminOrStaff, )
    
    def get(self, request, order_id):
        # Try to find in active orders first
        try:
            order = ActiveOrders.objects.select_related('user', 'item').get(order_id=order_id)
            is_completed = False
        except ActiveOrders.DoesNotExist:
            # Try past orders
            try:
                order = PastOrders.objects.select_related('user', 'item').get(order_id=order_id)
                is_completed = True
            except PastOrders.DoesNotExist:
                return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        
        data = {
            'order_id': order.order_id,
            'user_id': order.user.id if order.user else None,
            'user_name': order.user.name if order.user else 'Unknown',
            'user_email': order.user.email if order.user else 'N/A',
            'user_number': order.user.number if order.user else 'N/A',
            'item_id': order.item.id if order.item else None,
            'item_name': order.item.item if order.item else 'Unknown',
            'item_price': str(order.item.price) if order.item else '0',
            'quantity': order.quantity,
            'cost': str(order.cost),
            'custom_message': order.custom_message,
            'order_time': order.order_time,
            'is_completed': is_completed,
        }
        
        return Response(data, status=status.HTTP_200_OK)


class AdminGetPrintoutDetails(APIView):
    """Get detailed information for a specific printout"""
    permission_classes = (IsAdminOrStaff, )
    
    def get(self, request, order_id):
        # Try to find in active printouts first
        try:
            printout = ActivePrintOuts.objects.select_related('user').get(order_id=order_id)
            is_completed = False
        except ActivePrintOuts.DoesNotExist:
            # Try past printouts
            try:
                printout = PastPrintOuts.objects.select_related('user').get(order_id=order_id)
                is_completed = True
            except PastPrintOuts.DoesNotExist:
                return Response({'error': 'Printout not found'}, status=status.HTTP_404_NOT_FOUND)
        
        def count_pages_in_range(page_range_str):
            """Count total pages from a range string like '1-5,10-15' """
            if not page_range_str or page_range_str.strip() == '':
                return 0
            
            total = 0
            parts = page_range_str.split(',')
            for part in parts:
                part = part.strip()
                if '-' in part:
                    try:
                        start, end = part.split('-')
                        total += int(end) - int(start) + 1
                    except:
                        pass
                else:
                    try:
                        int(part)
                        total += 1
                    except:
                        pass
            return total
        
        bw_pages = count_pages_in_range(printout.black_and_white_pages)
        color_pages = count_pages_in_range(printout.coloured_pages)
        
        data = {
            'order_id': printout.order_id,
            'user_id': printout.user.id if printout.user else None,
            'user_name': printout.user.name if printout.user else 'Unknown',
            'user_email': printout.user.email if printout.user else 'N/A',
            'user_number': printout.user.number if printout.user else 'N/A',
            'coloured_pages': printout.coloured_pages,
            'black_and_white_pages': printout.black_and_white_pages,
            'print_on_one_side': printout.print_on_one_side,
            'total_pages': bw_pages + color_pages,
            'cost': str(printout.cost),
            'custom_message': printout.custom_message,
            'order_time': printout.order_time,
            'file': request.build_absolute_uri(printout.file.url) if printout.file else None,
            'is_completed': is_completed,
        }
        
        return Response(data, status=status.HTTP_200_OK)
