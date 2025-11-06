from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status

from . models import ActiveOrders, PastOrders, ActivePrintOuts, PastPrintOuts, Items
from . serializers import ActiveOrdersSerializer, PastOrdersSerializer, ActivePrintoutsSerializer, PastPrintoutsSerializer, ItemsSerializer
from . permissions import IsAdminOrStaff

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import tempfile

import os

from django.http import HttpResponse
    
from .calculate_cost import check_black_content
from .generate_firstpage import firstpage
from .pdf_watermark import watermark
from .img_to_pdf import img_to_pdf
from .word_to_pdf import docx_to_pdf








# To get all Items
class GetItemList(APIView):
    
    permission_classes = (IsAuthenticated, )

    def get(self, request):

        all_items = Items.objects.all()
        serializer = ItemsSerializer(all_items, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

# To get all active orders of the logged in user
class GetActiveOrders(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        
        user = request.user
        all_orders = ActiveOrders.objects.filter(user=user)
        serializer = ActiveOrdersSerializer(all_orders, many=True)
        orders_data = []

        for order in serializer.data:
            item = Items.objects.get(pk=order['item'])
            order['item_name'] = item.item
            order['item_display_image'] = item.display_image.url
            orders_data.append(order)

        return Response(orders_data, status=status.HTTP_200_OK)

# To get all past orders of the logged in user
class GetPastOrders(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        
        user = request.user
        all_orders = PastOrders.objects.filter(user=user)
        serializer = PastOrdersSerializer(all_orders, many=True)
        orders_data = []

        for order in serializer.data:
            item = Items.objects.get(pk=order['item'])
            order['item_name'] = item.item
            order['item_display_image'] = item.display_image.url
            orders_data.append(order)

        return Response(orders_data, status=status.HTTP_200_OK)

# To get all active printouts of the logged in user
class GetActivePrintouts(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        
        all_orders = ActivePrintOuts.objects.filter(user=request.user)
        serializer = ActivePrintoutsSerializer(all_orders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

# To get all past printouts of the logged in user
class GetPastPrintouts(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        
        all_orders = PastPrintOuts.objects.filter(user=request.user)
        serializer = PastPrintoutsSerializer(all_orders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# ==================== ADMIN ENDPOINTS ====================

class AdminGetAllActiveOrders(APIView):
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


class AdminDashboardStats(APIView):
    permission_classes = (IsAdminOrStaff, )
    
    def get(self, request):
        from django.utils import timezone
        from datetime import timedelta
        
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


class AdminGetAllPastOrders(APIView):
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





# To create a single order or multiple orders at once
class CreateOrder(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request):

        # key value pair is coming
        # key is named 'orders', value is a list of orders
        # {
        #   'orders': [ {'item' : RING_FILE, 'quantity': 2, 'cost': 40}, {'item' : PEN, 'quantity': 3, 'cost': 30}, ]
        # } 

        orders = request.data.get('orders')

        for order in orders:
            data = {
                'user' : request.user.pk,
                'item' : Items.objects.filter(item=order['item']).first().pk,
                'quantity' : int(order['quantity']),
                'cost' : float(order['cost']),
                'custom_message' : order['custom_message'],
            }

            serializer = ActiveOrdersSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
            else:
                return Response({'message': 'Order Creation Failed'}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({'message': 'Orders Created Successfully'}, status=status.HTTP_200_OK)

# To create a single printout order    
'''class CreatePrintout(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request):
        
        try:

            printouts_data = request.data.getlist('printouts', [])  # Assuming 'printouts' is the key for the list of printouts

            print("\n")
            print(type(printouts_data))

            for printout_data in printouts_data:
                print(type(printout_data))
                # file = printout_data.get('file')
                data = {
                    'user': request.user.pk,
                    'coloured_pages': printout_data.get('coloured_pages'),
                    'black_and_white_pages': printout_data.get('black_and_white_pages'),
                    'cost': float(printout_data.get('cost')),
                    'custom_message': printout_data.get('custom_message', ''),
                    'print_on_one_side': printout_data.get('print_on_one_side', True),
                    # 'file': file,
                }

                serializer = ActivePrintoutsSerializer(data=data)

                if serializer.is_valid():
                    serializer.save()
                else:
                    # If any printout fails validation, return the error message immediately
                    return Response({'message': 'Printout Order Creation Failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'message': 'Printout Orders Created Successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
'''

class CreatePrintout(APIView):

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
                    # If any printout fails validation, return the error message immediately
                    return Response({'message': 'Printout Order Creation Failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'message': 'Printout Orders Created Successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)



def parse_page_ranges(page_ranges):
    pages_to_check = []

    ranges = page_ranges.split(',')
    for item in ranges:
        if '-' in item:
            start, end = map(int, item.split('-'))
            pages_to_check.extend(range(start, end + 1))
        else:
            pages_to_check.append(int(item))
    
    return pages_to_check        
                
# To calculate cost for printouts   
# 2rs for b & w page
# 5rs for b & w page with output on it
# 5rs for coloured page
class CostCalculationView(APIView):
    
    def post(self, request):
        
        # Get the files array, b&w pages array, and coloured pages array
        files = request.FILES.getlist('files')
        pages = request.data.getlist('pages')
        coloured_pages = request.data.getlist('colouredpages')

        # initialize the cost to 0
        cost = 0

        try:
            # Perform the iteration for each file
            n = len(files)

            for i in range(n):
                file = files[i]
                page = pages[i]
                coloured_page = coloured_pages[i]

                # Save the file temporarily
                temp_file = default_storage.save('temp_files/' + file.name, ContentFile(file.read()))

                # Full path to the temporarily saved file
                temp_path = default_storage.path(temp_file)
                
                extension = str(temp_path).split('.')[-1] 
                
                # if the file is a pdf
                if (extension.lower() == 'pdf'):

                    black_pages, non_black_pages = check_black_content.check_black_content(pdf_path=temp_path, page_ranges=page)

                    cost += 2.0 * len(non_black_pages)
                    cost += 5.0 * len(black_pages)
                    cost += 10.0 * len(parse_page_ranges(coloured_page))
  
                    # Delete the temporarily saved file
                    default_storage.delete(temp_file)
                    
                # if the file is a word document
                elif (extension.lower() == 'docx'):
                    
                    # Convert DOCX to PDF using the utility function
                    pdf_data = docx_to_pdf.convert_docx_to_pdf(temp_path)
                    
                    if pdf_data:
                        # Save the converted PDF temporarily
                        temp_pdf_file = default_storage.save('temp_files/converted.pdf', ContentFile(pdf_data))
                        
                        # Full path to the temporarily saved PDF file
                        temp_pdf_path = default_storage.path(temp_pdf_file)
                        
                        # Proceed with cost calculation for the PDF file
                        black_pages, non_black_pages = check_black_content.check_black_content(pdf_path=temp_pdf_path, page_ranges=page)

                        cost += 2.0 * len(non_black_pages)
                        cost += 5.0 * len(black_pages)
                        cost += 10.0 * len(parse_page_ranges(coloured_page))
  
                        # Delete the temporarily saved files
                        default_storage.delete(temp_file)
                        default_storage.delete(temp_pdf_file)

                    else:
                        # Delete the temporarily saved file
                        default_storage.delete(temp_file)
                        return Response({'error': 'Failed to convert DOCX to PDF'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                
                else:
                    default_storage.delete(temp_file)
                    return Response({'error': 'Invalid file type. Only pdf and docx accepted'}, status=status.HTTP_400_BAD_REQUEST)                    

            # If everything goes OK, then return the cost
            return Response({'cost': cost}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
     



class FirstPageGenerationView(APIView):
    
    # permission_classes = (IsAuthenticated, )
    
    def post(self, request):
        
        try:
            subject_name = request.data.get('subject_name')
            subject_code = request.data.get('subject_code')
            faculty_name = request.data.get('faculty_name')
            student_name = request.data.get('student_name')
            faculty_designation = request.data.get('faculty_designation')
            roll_number = request.data.get('roll_number')
            semester = request.data.get('semester')
            group = request.data.get('group')
            image_path = 'maitlogomain.png'
            
            file_path = firstpage.create_word_file(subject_name=subject_name, subject_code=subject_code,
                                faculty_name=faculty_name, student_name=student_name, faculty_designation=faculty_designation,
                                roll_number=roll_number, semester=semester, group=group, image_path=image_path)  

            pdf_data = docx_to_pdf.convert_docx_to_pdf(file_path)

            # Create a response with PDF content?
            pdf_response = HttpResponse(pdf_data, content_type='application/pdf')
            pdf_response['Content-Disposition'] = 'attachment; filename="converted.pdf"'

            # Delete the temporary files
            os.remove(file_path)    

            return pdf_response
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
class ImageToPdfAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        image_files = request.FILES.getlist('images')
        pics_per_page = int(request.POST.get('pics_per_page', 2))  # Default value is 2 if not provided

        if not image_files:
            return Response({"error": "No images provided"}, status=400)

        try:
            # Create a temporary directory to store the images
            with tempfile.TemporaryDirectory() as temp_dir:
                # Save each image file to the temporary directory
                image_paths = []
                for image_file in image_files:
                    file_path = os.path.join(temp_dir, image_file.name)
                    with open(file_path, 'wb') as f:
                        for chunk in image_file.chunks():
                            f.write(chunk)
                    image_paths.append(file_path)

                # Generate PDF using the ImageToPdfConverter
                converter = img_to_pdf.ImageToPdfConverter(directory=temp_dir, pics_per_page=pics_per_page)
                pdf_content = converter.create_pdf()

                # Return the PDF as a response
                response = HttpResponse(pdf_content, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="output.pdf"'
                return response

        except Exception as e:
            return Response({"error": str(e)}, status=500)


# ==================== ADMIN INVENTORY MANAGEMENT ENDPOINTS ====================

class AdminUpdateItemStock(APIView):
    """
    Toggle item stock status (Admin/Staff only)
    """
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
    """
    Update item details (Admin/Staff only)
    """
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
    """
    Create new item (Admin/Staff only)
    """
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
    """
    Delete item (Admin/Staff only)
    """
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


# ==================== ADMIN ORDER MANAGEMENT ENDPOINTS ====================

class AdminCompleteOrder(APIView):
    """
    Mark an active order as completed (move to past orders) - Admin/Staff only
    """
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
    """
    Mark an active printout as completed (move to past printouts) - Admin/Staff only
    """
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


class AdminGetOrderDetails(APIView):
    """
    Get detailed information for a specific order (Admin/Staff only)
    """
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
    """
    Get detailed information for a specific printout (Admin/Staff only)
    """
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
        
        data = {
            'order_id': printout.order_id,
            'user_id': printout.user.id if printout.user else None,
            'user_name': printout.user.name if printout.user else 'Unknown',
            'user_email': printout.user.email if printout.user else 'N/A',
            'user_number': printout.user.number if printout.user else 'N/A',
            'coloured_pages': printout.coloured_pages,
            'black_and_white_pages': printout.black_and_white_pages,
            'print_on_one_side': printout.print_on_one_side,
            'total_pages': printout.coloured_pages + printout.black_and_white_pages,
            'cost': str(printout.cost),
            'custom_message': printout.custom_message,
            'order_time': printout.order_time,
            'file': request.build_absolute_uri(printout.file.url) if printout.file else None,
            'is_completed': is_completed,
        }
        
        return Response(data, status=status.HTTP_200_OK)
