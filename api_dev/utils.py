from django.http import JsonResponse
from pylovepdf.tools.imagetopdf import ImageToPdf
from django.views.decorators.csrf import csrf_exempt
from .utility import PUBLIC_KEY,IMAGE_PATH
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import imaplib
import email
import os
import tempfile
from django.conf import settings



# @csrf_exempt
# def convert_image_to_pdf_view(request):
#     print("test0")
#     if request.method == 'POST':
#         print("test1")
    
#         public_key = PUBLIC_KEY
#         print("test12")
       
#         t = ImageToPdf(public_key, verify_ssl=True,proxies= None)
#         image_file_path = IMAGE_PATH
#         # Add the image file to the task
#         t.add_file(image_file_path)
#         print("test3")
#         # task parameters
#         t.debug = False
#         t.orientation = 'portrait'
#         t.margin = 0
#         t.pagesize = 'fit'
#         print("output1")
#         # output
#         output_directory = 'C:/Users/richu/Documents/Practice_Django/pdf_proj/output_file'
#         print("output2")
#         t.set_output_folder(output_directory)
        
#         t.execute()
#         print("output3")

#         pdf_filename = t.download()

#         t.delete_current_task()

#         return JsonResponse({'pdf_filename': pdf_filename})
#     else:
#         return JsonResponse({'error': 'Only POST requests are supported'}, status=405)



def search_emails(sender, subject):
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(settings.EMAIL_HOST)
    mail.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    
    # Select the mailbox (inbox)
    mail.select('inbox')

    # Search for emails based on sender and subject
    result, data = mail.search(None, f'(FROM "{sender}" SUBJECT "{subject}")')
    
    email_texts = []
    
    if result == 'OK':
        for num in data[0].split():
            # Fetch the email
            result, data = mail.fetch(num, '(RFC822)')
            raw_email = data[0][1]
            
            # Parse the raw email data
            msg = email.message_from_bytes(raw_email)
            
            # Extract the email content
            email_text = ''
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        email_text += part.get_payload(decode=True).decode('utf-8')
            else:
                email_text = msg.get_payload(decode=True).decode('utf-8')
            
            email_texts.append(email_text)
    
    return email_texts




def generate_pdf_from_text(email_text):
    # Create a temporary directory to store the PDF file
    temp_dir = tempfile.mkdtemp()

    # Generate the PDF file
    output_file_full_path = os.path.join(temp_dir, 'email_pdf_output.pdf')
    with open(output_file_full_path, 'wb') as output_file:
        # Create a new PDF document using ReportLab
        pdf = SimpleDocTemplate(output_file, pagesize=letter)
        styles = getSampleStyleSheet()

        # Create a list of paragraphs from the email text
        email_paragraphs = [Paragraph(text, styles["Normal"]) for text in email_text.split("\n")]

        # Add the paragraphs to the PDF document
        pdf.build(email_paragraphs)

    # Return the full path to the generated PDF file
    return output_file_full_path





#   public_key = 'project_public_bc77f43cdd3f08c4a33667264b6eede6_F4hRd34b4a35b5d3fbdb2994e55c006e983ca'
#     image_file = 'C:/Users/richu/Documents/Practice_Django/pdf_proj/api_dev/image.jpg'
#     output_directory = 'C:/Users/richu/Documents/Practice_Django/pdf_proj'















# def retrieve_and_save_emails():
#     # Connect to the IMAP server
#     server = imapclient.IMAPClient(settings.EMAIL_HOST)
#     server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

#     # Select the mailbox (e.g., INBOX)
#     server.select_folder('INBOX')

#     # Search for emails
#     search_criteria = 'ALL'  # You can use different search criteria here
#     email_ids = server.search(search_criteria)

#     # Fetch and save emails
#     for email_id in email_ids:
#         raw_email = server.fetch(email_id, ['BODY[]'])
#         email_message = EmailMessage()
#         email_message.set_payload(raw_email[b'BODY[]'])

#         # Extract email data
#         subject = email_message['subject']
#         sender = email_message['from']
#         content = email_message.get_payload(decode=True).decode()

#         # Save email data to Django database
#         Email.objects.create(subject=subject, sender=sender, content=content)

#     # Disconnect from the IMAP server
#     server.logout()
