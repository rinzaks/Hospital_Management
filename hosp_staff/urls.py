from django.urls import path
from .views import (edit_employee,create_patient,view_my_patient,doc_edit_patient,edit_my_profile,create_company_location, delete_employee, staff_login, all_appointments, admin_dashboard, create_staff,edit_admin_profile,patient_delete_appointment,edit_patient_appointment,
                    staff_logout,my_patients, doctors_list,patients_list,all_schedules, employees, staff_selection,create_department,view_myprofile,
                    departments, edit_department, delete_department, view_employee,reset_password,add_availability, delete_availability,admin_receptionist_add_appointment,
                    edit_availability, edit_patient, delete_patient, doctor_dashboard,nurse_dashboard,receptionist_dashboard,my_schedules)


urlpatterns =[
    path('staff_selection/', staff_selection, name='staff_selection'),
    path('patient/edit/<int:patient_id>/', doc_edit_patient, name='doc_edit_patient'),
    path('view_my_patient/<int:patient_id>/', view_my_patient, name='view_my_patient'),
    path('reset_password/', reset_password, name='reset_password'),
    path('edit_admin_profile/',edit_admin_profile, name='edit_admin_profile'),
    path('edit_patient/<int:patient_id>/', edit_patient, name='edit_patient'),
    path('delete_patient/<int:patient_id>/', delete_patient, name='delete_patient'),
    path('login/', staff_login, name='staff_login'),
    path('all_appointments/', all_appointments, name='all_appointments'),
    path('create_staff/<str:staff_type>/', create_staff, name='create_staff'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('doctor_dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('nurse_dashboard/', nurse_dashboard, name='nurse_dashboard'),
    path('receptionist_dashboard/', receptionist_dashboard, name='receptionist_dashboard'),
    path('doctors_list/', doctors_list, name='doctors_list'),
    path('patients_list/', patients_list, name='patients_list'),
    path('logout/', staff_logout, name='staff_logout'),  # Add this line
    path('create_department/', create_department, name='add_department'),
    path('departments/', departments, name='departments'),
    path('edit_department/<int:department_id>/', edit_department, name='edit_department'),
    path('delete_department/<int:department_id>/', delete_department, name='delete_department'),
    path('employees/', employees, name='employees'),
    path('hosp_staff/view_employee/<int:employee_id>/', view_employee, name='view_employee'),
    path('employee/edit/<int:employee_id>/', edit_employee, name='edit_employee'),
    path('hosp_staffemployee/delete/<int:employee_id>/', delete_employee, name='delete_employee'),
    path('add_availability/', add_availability, name='add_availability'),
    path('edit_availability/<int:availability_id>/', edit_availability, name='edit_availability'),
    path('availability/delete/<int:availability_id>/', delete_availability, name='delete_availability'),
    path('view_myprofile/', view_myprofile, name='view_myprofile'),
    path('all_schedules/', all_schedules, name='all_schedules'), 
    path('my_schedules/', my_schedules, name='my_schedules'), 
    path('my_patients/', my_patients, name='my_patients'), 
    path('edit_patient_appointments<int:appointment_id>/', edit_patient_appointment, name='edit_patient_appointment'),
    path('patient_delete_appointment/<int:appointment_id>/', patient_delete_appointment, name='patient_delete_appointment'), # Example
    path('admin_receptionist_add_appointment/', admin_receptionist_add_appointment, name='admin_receptionist_add_appointment'),
    path('create_company_location/', create_company_location, name='create_company_location'), # Example
    path('edit_my_profile/', edit_my_profile, name='edit_my_profile'), # Example
    path('create_patient/', create_patient, name='create_patient'), # Example


]


