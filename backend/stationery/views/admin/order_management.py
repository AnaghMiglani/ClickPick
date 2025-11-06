"""
Admin order management endpoints for completing/processing orders
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ...models import ActiveOrders, PastOrders, ActivePrintOuts, PastPrintOuts
from ...permissions import IsAdminOrStaff


class AdminCompleteOrder(APIView):
    """Mark an active order as completed (move to past orders) """
    permission_classes = (IsAdminOrStaff, )
    
    def post(self, request, order_id):
        try:
            active_order = ActiveOrders.objects.get(order_id=order_id)
            
            # Create past order with same data
            past_order = PastOrders(
                order_id=order_id,
                user=active_order.user,
                item=active_order.item,
                quantity=active_order.quantity,
                cost=active_order.cost,
                custom_message=active_order.custom_message,
                order_time=active_order.order_time
            )
            past_order.save()
            
            # Delete from active orders
            active_order.delete()
            
            return Response({
                'message': 'Order marked as completed',
                'order_id': order_id
            }, status=status.HTTP_200_OK)
        except ActiveOrders.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


class AdminCompletePrintout(APIView):
    """Mark an active printout as completed (move to past printouts) """
    permission_classes = (IsAdminOrStaff, )
    
    def post(self, request, order_id):
        try:
            active_printout = ActivePrintOuts.objects.get(order_id=order_id)
            
            # Create past printout with same data
            past_printout = PastPrintOuts(
                order_id=order_id,
                user=active_printout.user,
                coloured_pages=active_printout.coloured_pages,
                black_and_white_pages=active_printout.black_and_white_pages,
                print_on_one_side=active_printout.print_on_one_side,
                cost=active_printout.cost,
                custom_message=active_printout.custom_message,
                order_time=active_printout.order_time,
                file=active_printout.file
            )
            past_printout.save()
            
            # Delete from active printouts
            active_printout.delete()
            
            return Response({
                'message': 'Printout marked as completed',
                'order_id': order_id
            }, status=status.HTTP_200_OK)
        except ActivePrintOuts.DoesNotExist:
            return Response({'error': 'Printout not found'}, status=status.HTTP_404_NOT_FOUND)
