from django.urls import path
from . import views

urlpatterns = [
    #path('send/', views.send_test_email),
   # path('convertpdf/', views.your_view_function),
    path('', views.search_email, name='search_email'),  # URL for the search form
    path('search-results/', views.search_results, name='search_results'),  # URL for displaying search results
]