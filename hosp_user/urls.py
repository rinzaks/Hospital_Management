from django.urls import path
from .views import (login_patient, patient_home,changepassword,user_logout,edit_myprofile
                    ,schedule_view,my_appointments,delete_profile,edit_appointment,delete_appointment,patient_add_appointment)

urlpatterns = [
    path('login_patient/', login_patient, name='login_patient'),  
    path('patient_home/', patient_home, name='patient_home'),  # Updated to match your previous references
    path('changepassword/', changepassword, name='changepassword'),
    path('user_logout/', user_logout, name='user_logout'),  
    path('edit_myprofile/', edit_myprofile, name='edit_myprofile'),  
    path('schedule_view/', schedule_view, name='schedule_view'),
    path('my_appointments/', my_appointments, name='my_appointments'),
    path('delete_profile/', delete_profile, name='delete_profile'),
    path('patient_add_appointment/', patient_add_appointment, name='patient_add_appointment'),
    path('edit_appointment/<int:appointment_id>/', edit_appointment, name='edit_appointment'),
    path('delete_appointment/<int:appointment_id>/', delete_appointment, name='delete_appointment'),


]
