from django.urls import path
from .import views
app_name = 'Basics'

urlpatterns = [
    path('Calculator/', views.calculator, name='Calculator'),
    path('Largest/', views.largest, name='Largest'),
    path('Largestof3/', views.largestof3, name='Largestof3'),
    path('Sum/', views.Sum, name='Sum'),
]
