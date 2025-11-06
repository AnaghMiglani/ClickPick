"""
Admin inventory management endpoints for items/products
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ...models import Items
from ...serializers import ItemsSerializer
from ...permissions import IsAdminOrStaff


class AdminUpdateItemStock(APIView):
    """Toggle item stock status """
    permission_classes = (IsAdminOrStaff, )
    
    def patch(self, request, item_id):
        try:
            item = Items.objects.get(id=item_id)
            item.in_stock = not item.in_stock
            item.save()
            
            return Response({
                'message': 'Item stock status updated',
                'item_id': item.id,
                'in_stock': item.in_stock
            }, status=status.HTTP_200_OK)
        except Items.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)


class AdminUpdateItem(APIView):
    """Update item details """
    permission_classes = (IsAdminOrStaff, )
    
    def put(self, request, item_id):
        try:
            item = Items.objects.get(id=item_id)
            
            # Update allowed fields
            if 'item' in request.data:
                item.item = request.data['item']
            if 'price' in request.data:
                item.price = request.data['price']
            if 'in_stock' in request.data:
                item.in_stock = request.data['in_stock']
            
            item.save()
            
            serializer = ItemsSerializer(item)
            return Response({
                'message': 'Item updated successfully',
                'item': serializer.data
            }, status=status.HTTP_200_OK)
        except Items.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)


class AdminCreateItem(APIView):
    """Create new item """
    permission_classes = (IsAdminOrStaff, )
    
    def post(self, request):
        serializer = ItemsSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Item created successfully',
                'item': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminDeleteItem(APIView):
    """Delete item """
    permission_classes = (IsAdminOrStaff, )
    
    def delete(self, request, item_id):
        try:
            item = Items.objects.get(id=item_id)
            item_name = item.item
            item.delete()
            
            return Response({
                'message': f'Item "{item_name}" deleted successfully'
            }, status=status.HTTP_200_OK)
        except Items.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
