from rest_framework.decorators import api_view
from rest_framework.response import Response
from pylovepdf.tools.merge import Merge
from django.views.decorators.csrf import csrf_exempt
from .asset import PUBLIC_KEY,OUTPUT_PATH,IMAGE_PATH
from django.http import JsonResponse
from pylovepdf.tools.imagetopdf import ImageToPdf
from pylovepdf.tools.compress import Compress
from pylovepdf.tools.pdftojpg import PdfToJpg

@api_view(['GET'])
def getroutes(request):
    
    routes = [
        {'GET': '/api/members/'},        # Retrieve all members
        {'GET': '/api/members/<id>'},    # Retrieve a specific member
        {'POST': '/api/members/'},       # Create a new member
        {'PUT': '/api/members/<id>'},    # Update a specific member (replace entire resource)
        {'PATCH': '/api/members/<id>'},  # Update a specific member (partially)
        {'DELETE': '/api/members/<id>'},    
    ]
    #return JsonResponse(routes, safe=False)
    return Response(routes)

@csrf_exempt
@api_view(['POST'])
def merge_pdf_view(request):
    if request.method == 'POST':
        public_key = PUBLIC_KEY
        output = OUTPUT_PATH
        pdf_paths = [
            'C:/Users/richu/Documents/Practice_Django/pdf_proj/pdf_coll/meg1.pdf',
            'C:/Users/richu/Documents/Practice_Django/pdf_proj/pdf_coll/meg2.pdf',
        ]
        # Create an instance of Merge task
        t = Merge(public_key, verify_ssl=True,proxies=None)

        # Add each PDF file using its path to the task
        for pdf_path in pdf_paths:
            t.add_file(pdf_path)

        # task parameters
        t.debug = False
        t.set_output_folder(output)
        t.execute()

        pdf_filename = t.download()
        #t.delete_current_task()

        return Response({'pdf_filename': pdf_filename})
    else:
        return Response({'error': 'Only POST requests are supported'}, status=405)


@csrf_exempt
@api_view(['POST'])
def convert_image_to_pdf_view(request):
    if request.method == 'POST':
        print("test")
        public_key = PUBLIC_KEY
        t = ImageToPdf(public_key, verify_ssl=True,proxies= None)
        image_file_path = IMAGE_PATH
        t.add_file(image_file_path)
        # task parameters
        t.debug = False
        t.orientation = 'portrait'
        t.margin = 0
        t.pagesize = 'fit'
        print("output1")
        # output
        output_directory = OUTPUT_PATH
        t.set_output_folder(output_directory)
        t.execute()

        pdf_filename = t.download()
        t.delete_current_task()

        return JsonResponse({'pdf_filename': pdf_filename})
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)
    


@csrf_exempt
@api_view(['POST'])
def compress_pdf(request):
    if request.method == 'POST':
        public_key = PUBLIC_KEY
        t = Compress(public_key, verify_ssl=True,proxies= None)
        t.add_file('C:/Users/richu/Documents/Practice_Django/pdf_proj/pdf_coll/meg1.pdf')
        # task parameters
        t.debug = False
        t.compression_level = 'low'
        # output
        output_directory = OUTPUT_PATH
        t.set_output_folder(output_directory)
        t.execute()

        pdf_filename = t.download()
        t.delete_current_task()

        return JsonResponse({'pdf_filename': pdf_filename})
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)
     

@csrf_exempt
@api_view(['POST'])
def convert_pdf_to_img(request):
    if request.method == 'POST':
        print("test")
        public_key = PUBLIC_KEY
        t = PdfToJpg(public_key, verify_ssl=True,proxies= None)
        t.add_file('C:/Users/richu/Documents/Practice_Django/pdf_proj/output_file/merge_13-03-2024.pdf')
        # task parameters2.
        t.debug = False
        t.pdfjpg_mode = 'pages'
        # output
        output_directory = OUTPUT_PATH
        t.set_output_folder(output_directory)
        t.execute()
        pdf_filename = t.download()

        return JsonResponse({'pdf_filename': pdf_filename})
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)


    

