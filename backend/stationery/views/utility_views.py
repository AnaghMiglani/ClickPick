"""
Utility API endpoints for cost calculation, PDF generation, and image conversion
"""
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse

import tempfile
import os

from ..calculate_cost import check_black_content
from ..generate_firstpage import firstpage
from ..pdf_watermark import watermark
from ..img_to_pdf import img_to_pdf
from ..word_to_pdf import docx_to_pdf


def parse_page_ranges(page_ranges):
    """Parse page range strings like '1-5,7,9-12' into list of page numbers"""
    pages_to_check = []

    ranges = page_ranges.split(',')
    for item in ranges:
        if '-' in item:
            start, end = map(int, item.split('-'))
            pages_to_check.extend(range(start, end + 1))
        else:
            pages_to_check.append(int(item))
    
    return pages_to_check


class CostCalculationView(APIView):
    """
    Calculate cost for printouts based on page types and colors
    Pricing:
    - Black & white page (with content): 2rs
    - Black & white page (with output): 5rs
    - Colored page: 10rs
    """
    
    def post(self, request):
        # Get the files array, b&w pages array, and coloured pages array
        files = request.FILES.getlist('files')
        pages = request.data.getlist('pages')
        coloured_pages = request.data.getlist('colouredpages')

        # Initialize the cost to 0
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
                
                # If the file is a PDF
                if extension.lower() == 'pdf':
                    black_pages, non_black_pages = check_black_content.check_black_content(
                        pdf_path=temp_path, 
                        page_ranges=page
                    )

                    cost += 2.0 * len(non_black_pages)
                    cost += 5.0 * len(black_pages)
                    cost += 10.0 * len(parse_page_ranges(coloured_page))
  
                    # Delete the temporarily saved file
                    default_storage.delete(temp_file)
                    
                # If the file is a Word document
                elif extension.lower() == 'docx':
                    # Convert DOCX to PDF using the utility function
                    pdf_data = docx_to_pdf.convert_docx_to_pdf(temp_path)
                    
                    if pdf_data:
                        # Save the converted PDF temporarily
                        temp_pdf_file = default_storage.save('temp_files/converted.pdf', ContentFile(pdf_data))
                        
                        # Full path to the temporarily saved PDF file
                        temp_pdf_path = default_storage.path(temp_pdf_file)
                        
                        # Proceed with cost calculation for the PDF file
                        black_pages, non_black_pages = check_black_content.check_black_content(
                            pdf_path=temp_pdf_path, 
                            page_ranges=page
                        )

                        cost += 2.0 * len(non_black_pages)
                        cost += 5.0 * len(black_pages)
                        cost += 10.0 * len(parse_page_ranges(coloured_page))
  
                        # Delete the temporarily saved files
                        default_storage.delete(temp_file)
                        default_storage.delete(temp_pdf_file)
                    else:
                        # Delete the temporarily saved file
                        default_storage.delete(temp_file)
                        return Response(
                            {'error': 'Failed to convert DOCX to PDF'}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
                else:
                    default_storage.delete(temp_file)
                    return Response(
                        {'error': 'Invalid file type. Only pdf and docx accepted'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )                    

            # If everything goes OK, then return the cost
            return Response({'cost': cost}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FirstPageGenerationView(APIView):
    """Generate formatted first page for academic documents"""
    
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
            
            file_path = firstpage.create_word_file(
                subject_name=subject_name, 
                subject_code=subject_code,
                faculty_name=faculty_name, 
                student_name=student_name, 
                faculty_designation=faculty_designation,
                roll_number=roll_number, 
                semester=semester, 
                group=group, 
                image_path=image_path
            )  

            pdf_data = docx_to_pdf.convert_docx_to_pdf(file_path)

            # Create a response with PDF content
            pdf_response = HttpResponse(pdf_data, content_type='application/pdf')
            pdf_response['Content-Disposition'] = 'attachment; filename="converted.pdf"'

            # Delete the temporary files
            os.remove(file_path)    

            return pdf_response
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ImageToPdfAPIView(APIView):
    """Convert multiple images to a single PDF"""
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        image_files = request.FILES.getlist('images')
        pics_per_page = int(request.POST.get('pics_per_page', 2))  # Default value is 2

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
                converter = img_to_pdf.ImageToPdfConverter(
                    directory=temp_dir, 
                    pics_per_page=pics_per_page
                )
                pdf_content = converter.create_pdf()

                # Return the PDF as a response
                response = HttpResponse(pdf_content, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="output.pdf"'
                return response

        except Exception as e:
            return Response({"error": str(e)}, status=500)
