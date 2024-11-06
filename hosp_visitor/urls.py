from django.urls import path
from .views import home,about,services,doctors,contact,register,custom_404_view

urlpatterns = [
path('',home,name='home'),
path('about/',about,name='about'),
path('services/',services,name='services'),
path('doctors/',doctors,name='doctors'),
path('contact/',contact,name='contact'),
path('register/', register, name='register'),
path('404/',custom_404_view,name='404')

]
