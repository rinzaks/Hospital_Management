from django.db import models
from django.contrib.auth.models import User
import uuid

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30) # Add this line for the name field
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    eid_num = models.CharField(max_length=20, unique=True)
    dob = models.DateField(null=True)
    mob_num = models.CharField(max_length=15, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # Field for soft deletion
    deleted_at = models.DateTimeField(null=True, blank=True)   # New field


    def __str__(self):
        return self.user.first_name

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_histories')
    illness = models.TextField(blank=True)
    surgeries = models.TextField(blank=True)
    hospitalizations = models.TextField(blank=True)
    family_medical_history = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Medical history for {self.patient.user.first_name}"
    
class Appointment(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    appointment_id = models.CharField(max_length=20, unique=True, editable=False, default='APT-001')
    doctor = models.ForeignKey('hosp_staff.Doctor', on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ], default='scheduled')  # Add status field

    def save(self, *args, **kwargs):
        if not self.appointment_id:
            self.appointment_id = f"APT-{uuid.uuid4().hex[:8].upper()}"  # Generates a unique ID
        super().save(*args, **kwargs)  # Call the superclass save method

    def __str__(self):
        return f'Appointment ID: {self.id} for {self.patient.user.get_full_name()} with {self.doctor}'

    class Meta:
        ordering = ['appointment_date']