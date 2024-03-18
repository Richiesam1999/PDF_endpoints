from django.urls import path
from . import views

urlpatterns = [

    path('',views.getroutes),         ##api url mapping, root empty url maps anything we enter 
    path('merge-pdf/', views.merge_pdf_view),
    path('convert-pdf/', views.convert_image_to_pdf_view),  # Endpoint to create a new member
    path('compress-pdf/', views.compress_pdf),
    path('convert-jpg/', views.convert_pdf_to_img),
]

