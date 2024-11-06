from django.contrib import admin
from .models import Patient,Appointment,MedicalHistory

admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(MedicalHistory)# Register your models here.

