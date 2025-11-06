"""
Student-facing API endpoints for orders and printouts
"""
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..models import ActiveOrders, PastOrders, ActivePrintOuts, PastPrintOuts, Items
from ..serializers import (
    ActiveOrdersSerializer, 
    PastOrdersSerializer, 
    ActivePrintoutsSerializer, 
    PastPrintoutsSerializer, 
    ItemsSerializer
)


class GetItemList(APIView):
    """Get all available items"""
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        all_items = Items.objects.all()
        serializer = ItemsSerializer(all_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetActiveOrders(APIView):
    """Get all active orders of the logged in user"""
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        all_orders = ActiveOrders.objects.filter(user=user)
        serializer = ActiveOrdersSerializer(all_orders, many=True)
        orders_data = []

        for order in serializer.data:
            item = Items.objects.get(pk=order['item'])
            order['item_name'] = item.item
            order['item_display_image'] = item.display_image.url if item.display_image else None
            orders_data.append(order)

        return Response(orders_data, status=status.HTTP_200_OK)


class GetPastOrders(APIView):
    """Get all past orders of the logged in user"""
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        all_orders = PastOrders.objects.filter(user=user)
        serializer = PastOrdersSerializer(all_orders, many=True)
        orders_data = []

        for order in serializer.data:
            item = Items.objects.get(pk=order['item'])
            order['item_name'] = item.item
            order['item_display_image'] = item.display_image.url if item.display_image else None
            orders_data.append(order)

        return Response(orders_data, status=status.HTTP_200_OK)


class GetActivePrintouts(APIView):
    """Get all active printouts of the logged in user"""
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        all_orders = ActivePrintOuts.objects.filter(user=request.user)
        serializer = ActivePrintoutsSerializer(all_orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetPastPrintouts(APIView):
    """Get all past printouts of the logged in user"""
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        all_orders = PastPrintOuts.objects.filter(user=request.user)
        serializer = PastPrintoutsSerializer(all_orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateOrder(APIView):
    """Create single or multiple orders at once"""
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        # Expected format:
        # {
        #   'orders': [ 
        #     {'item': 'RING_FILE', 'quantity': 2, 'cost': 40, 'custom_message': '...'}, 
        #     {'item': 'PEN', 'quantity': 3, 'cost': 30, 'custom_message': '...'}, 
        #   ]
        # } 

        orders = request.data.get('orders')

        for order in orders:
            data = {
                'user': request.user.pk,
                'item': Items.objects.filter(item=order['item']).first().pk,
                'quantity': int(order['quantity']),
                'cost': float(order['cost']),
                'custom_message': order['custom_message'],
            }

            serializer = ActiveOrdersSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
            else:
                return Response(
                    {'message': 'Order Creation Failed'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        return Response(
            {'message': 'Orders Created Successfully'}, 
            status=status.HTTP_200_OK
        )


class CreatePrintout(APIView):
    """Create printout orders with file uploads"""
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        # Get the files array, b&w pages array, and coloured pages array
        files = request.FILES.getlist('files')
        black_and_white_pages = request.data.getlist('pages')
        coloured_pages = request.data.getlist('colouredpages')
        costs = request.data.getlist('costs')
        print_on_one_side_list = request.data.getlist('print_on_one_side_list')
        custom_messages = request.data.getlist('custom_messages')

        try:
            # Perform the iteration for each file
            n = len(files)

            for i in range(n):
                file = files[i]
                black_and_white_page = black_and_white_pages[i]
                coloured_page = coloured_pages[i]
                cost = costs[i]
                print_on_one_side = print_on_one_side_list[i]
                custom_message = custom_messages[i]
                
                data = {
                    'user': request.user.pk,
                    'coloured_pages': coloured_page,
                    'black_and_white_pages': black_and_white_page,
                    'cost': float(cost),
                    'custom_message': custom_message,
                    'print_on_one_side': print_on_one_side,
                    'file': file,
                }

                serializer = ActivePrintoutsSerializer(data=data)

                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(
                        {
                            'message': 'Printout Order Creation Failed', 
                            'errors': serializer.errors
                        }, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            return Response(
                {'message': 'Printout Orders Created Successfully'}, 
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
