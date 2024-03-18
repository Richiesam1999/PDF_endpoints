from django.shortcuts import render
from .models import Email
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import get_connection, EmailMessage
from .utils import generate_pdf_from_text
from .utils import convert_image_to_pdf_view
from django.shortcuts import get_object_or_404
import email
from .utils import search_emails, generate_pdf_from_text
from django.http import FileResponse


# @csrf_exempt
# def your_view_function(request):
#     print("arghh")
#     if request.method == 'POST':
#         print("test")
#         # Call to convert_image_to_pdf_view function
#         return convert_image_to_pdf_view(request)
#     else:
#         return JsonResponse({'error': 'Only POST requests are supported'}, status=405)


# views.py

def search_email(request):
    return render(request, 'api_dev/search.html')

def search_results(request):
    if request.method == 'POST':
        sender = request.POST.get('sender')
        subject = request.POST.get('subject')

        # Perform search based on sender and subject
        email_texts = search_emails(sender, subject)

        # Convert email content to PDF and save to database
        for email_text in email_texts:
            pdf_content = generate_pdf_from_text(email_text)

            # Save PDF content and other information to database
            email = Email.objects.create(
                sender=sender,
                subject=subject,
                content=email_text,
            )
        
        return FileResponse(open(pdf_content, 'rb'), as_attachment=True)
        #return JsonResponse({'message': 'Search results saved to database'})
    else:
        return render(request, 'api_dev/search.html')




















# # Example usage:
# sender = 'sender@example.com'
# subject = 'Example Subject'
# email_texts = search_emails(sender, subject)
# for text in email_texts:
#     print(text)










# @csrf_exempt
# def convert_email_to_pdf(request):
#     if request.method == 'POST':
#         # Extract parameters from request body
#         subject = request.POST.get('subject')
#         sender_email = request.POST.get('sender')
#         email_text = request.POST.get('email_text')

#         # Check if an email with the given subject and recipient already exists
#         existing_email = Email.objects.filter(subject=subject, sender=sender_email).first()

#         if not existing_email:
#             # If the email does not exist, create a new Email object and save it to the database
#             new_email = Email.objects.create(subject=subject, sender=sender_email, content=email_text)
#         else:
#             # If the email already exists, update its content
#             existing_email.content = email_text
#             existing_email.save()

#         # Generate PDF from email text
#         pdf_content = generate_pdf_from_text(email_text)

#         return JsonResponse({'pdf_content': pdf_content})
#     else:
#         return JsonResponse({'error': 'Only POST requests are supported'}, status=405)