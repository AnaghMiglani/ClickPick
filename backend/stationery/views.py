from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
import json

from . models import ActiveOrders, PastOrders, ActivePrintOuts, PastPrintOuts, Items
from . serializers import ActiveOrdersSerializer, PastOrdersSerializer, ActivePrintoutsSerializer, PastPrintoutsSerializer, ItemsSerializer

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
        
        # Helper to safely extract list-like fields whether they come as
        # an actual list, a JSON string, a comma-separated string, or a
        # QueryDict (which supports getlist).
        def _get_list(key):
            # If request.FILES has the key (for file lists), prefer that
            if key == 'files':
                return request.FILES.getlist('files')

            # If request.data is a QueryDict it has getlist
            data = request.data
            try:
                # QueryDict has getlist
                return data.getlist(key)
            except Exception:
                pass

            # Support common alias spelling for coloured/colored
            value = data.get(key, [])
            if (value is None or value == []) and key == 'colouredpages':
                # try American spelling as fallback
                value = data.get('coloredpages', [])
            if isinstance(value, list):
                return value
            if value is None:
                return []
            if isinstance(value, str):
                # Try JSON decode first
                try:
                    parsed = json.loads(value)
                    if isinstance(parsed, list):
                        return parsed
                except Exception:
                    pass
                # For page-range fields we must NOT split commas because
                # the range syntax itself uses commas (e.g. '1-3,5').
                if key in ('pages', 'colouredpages'):
                    return [value]
                # Fallback to comma-separated for other keys
                return [v.strip() for v in value.split(',') if v.strip()]
            # Other scalar values
            return [value]

        # Get the files array, b&w pages array, and coloured pages array
        files = _get_list('files')
        black_and_white_pages = _get_list('pages')
        coloured_pages = _get_list('colouredpages')
        costs = _get_list('costs')
        print_on_one_side_list = _get_list('print_on_one_side_list')
        custom_messages = _get_list('custom_messages')

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
        # Reuse the same robust extractor used above (but define locally
        # in case this module is imported and the CreatePrintout helper
        # is not available at runtime). It mirrors the behavior of
        # QueryDict.getlist when available and falls back to parsing
        # strings or JSON lists.
        def _get_list_local(key):
            if key == 'files':
                # Prefer getlist but fall back to single-file or any uploaded files
                try:
                    fl = request.FILES.getlist('files')
                except Exception:
                    fl = None
                if fl:
                    return fl
                # direct key
                single = request.FILES.get('files')
                if single:
                    return [single]
                # otherwise return all uploaded files as a list
                return list(request.FILES.values())
            data = request.data
            try:
                return data.getlist(key)
            except Exception:
                pass
            value = data.get(key, [])
            if (value is None or value == []) and key == 'colouredpages':
                value = data.get('coloredpages', [])
            if isinstance(value, list):
                return value
            if value is None:
                return []
            if isinstance(value, str):
                try:
                    parsed = json.loads(value)
                    if isinstance(parsed, list):
                        return parsed
                except Exception:
                    pass
                # For page-range fields we must NOT split commas because
                # the range syntax itself uses commas (e.g. '1-3,5').
                if key in ('pages', 'colouredpages'):
                    return [value]
                return [v.strip() for v in value.split(',') if v.strip()]
            return [value]

        files = _get_list_local('files')
        pages = _get_list_local('pages')
        coloured_pages = _get_list_local('colouredpages')

        # Ensure files is always a list
        if not isinstance(files, list):
            files = [files]

        if len(files) == 0:
            return Response({'error': 'No files provided'}, status=status.HTTP_400_BAD_REQUEST)

        # initialize the cost to 0
        cost = 0

        try:
            # Perform the iteration for each file
            n = len(files)

            for i in range(n):
                try:
                    file = files[i]
                    page = pages[i]
                    coloured_page = coloured_pages[i]
                except IndexError:
                    # Provide a clear error message showing lengths to aid debugging
                    return Response({'error': 'Per-file parameter count mismatch',
                                     'files_count': n,
                                     'pages_count': len(pages) if isinstance(pages, list) else 1,
                                     'coloured_pages_count': len(coloured_pages) if isinstance(coloured_pages, list) else 1},
                                    status=status.HTTP_400_BAD_REQUEST)

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