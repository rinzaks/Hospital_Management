from django.contrib import admin
from .models import Department, Employee, Doctor, Nurse,Availability,Receptionist,AdminProfile

admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Receptionist)
admin.site.register(Availability)
admin.site.register(AdminProfile)
