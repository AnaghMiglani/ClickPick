from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
import os

from ...models import ActivePrintOuts, PastPrintOuts
from ...permissions import IsAdminOrStaff


class SecureFileDownload(APIView):
    """
    file download endpoint that requires admin/staff authentication.
    Only allows downloading files associated with printout orders.
    """
    permission_classes = (IsAdminOrStaff, )
    
    def get(self, request, order_id):
        try:
            printout = ActivePrintOuts.objects.get(order_id=order_id)
        except ActivePrintOuts.DoesNotExist:
            try:
                printout = PastPrintOuts.objects.get(order_id=order_id)
            except PastPrintOuts.DoesNotExist:
                return Response({'error': 'Printout not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if not printout.file:
            return Response({'error': 'No file associated with this order'}, status=status.HTTP_404_NOT_FOUND)
        
        file_path = printout.file.path
        
        if not os.path.exists(file_path):
            return Response({'error': 'File not found on server'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        except Exception as e:
            return Response({'error': f'Error serving file: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
