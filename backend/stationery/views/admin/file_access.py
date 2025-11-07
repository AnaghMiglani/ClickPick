from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
import os

from ...models import ActivePrintOuts, PastPrintOuts, PrintoutFile
from ...permissions import IsAdminOrStaff


class SecureFileDownload(APIView):
    """
    Secure file download endpoint that requires admin/staff authentication.
    Only allows downloading files associated with printout orders.
    """
    permission_classes = (IsAdminOrStaff, )
    
    def get(self, request, order_id):
        printout = None
        
        try:
            printout = ActivePrintOuts.objects.get(order_id=order_id)
        except ActivePrintOuts.DoesNotExist:
            try:
                printout = PastPrintOuts.objects.get(order_id=str(order_id))
            except PastPrintOuts.DoesNotExist:
                return Response({
                    'error': 'Printout not found',
                    'order_id': order_id,
                    'detail': f'No printout found with order_id={order_id} in active or past printouts'
                }, status=status.HTTP_404_NOT_FOUND)
        
        if not printout.file:
            return Response({
                'error': 'No file associated with this order',
                'order_id': order_id
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            file_path = printout.file.path
        except Exception as e:
            return Response({
                'error': 'Error accessing file path',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if not os.path.exists(file_path):
            return Response({
                'error': 'File not found on server',
                'file_path': file_path,
                'detail': f'File exists in database but not on filesystem'
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        except Exception as e:
            return Response({
                'error': 'Error serving file',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PrintoutFileDownload(APIView):
    """
    Download individual files from PrintoutFile model by file ID.
    """
    permission_classes = (IsAdminOrStaff, )
    
    def get(self, request, file_id):
        try:
            printout_file = PrintoutFile.objects.select_related(
                'printout_active', 
                'printout_past'
            ).get(id=file_id)
        except PrintoutFile.DoesNotExist:
            return Response({
                'error': 'File not found',
                'file_id': file_id,
                'detail': f'No file found with id={file_id}'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if not printout_file.file:
            return Response({
                'error': 'No file associated with this record',
                'file_id': file_id
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            file_path = printout_file.file.path
        except Exception as e:
            return Response({
                'error': 'Error accessing file path',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if not os.path.exists(file_path):
            return Response({
                'error': 'File not found on server',
                'file_path': file_path,
                'detail': 'File exists in database but not on filesystem'
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            response = FileResponse(open(file_path, 'rb'))
            filename = printout_file.file_name or os.path.basename(file_path)
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        except Exception as e:
            return Response({
                'error': 'Error serving file',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
