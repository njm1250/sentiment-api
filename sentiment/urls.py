from django.urls import path
from . import views

urlpatterns = [
    path('query/', views.query, name='query'),
    path('links/', views.links, name='links'),  
]