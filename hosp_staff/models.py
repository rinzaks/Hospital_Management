from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    # Add any other fields you need

    def __str__(self):
        return self.user.username
    
class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    dep_image = models.ImageField(upload_to='departments', blank=True, null=True)
    status = models.BooleanField(default=True)  # True for Active, False for Inactive


    def __str__(self):
        return self.name

class CompanyLocation(models.Model):
    company_name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

User = get_user_model()

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=100, unique=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    joining_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)  # New field to indicate active/inactive status
    deleted_at = models.DateTimeField(null=True, blank=True)  # Field to track when the record was marked as deleted

    def __str__(self):
        return f'{self.user.get_full_name()} - ID: {self.employee_id}'

    def get_staff_type(self):
        if hasattr(self, 'doctor'):
            return 'Doctor'
        elif hasattr(self, 'receptionist'):
            return 'Receptionist'
        elif hasattr(self, 'nurse'):
            return 'Nurse'
        return 'Unknown'

class Doctor(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    doc_image = models.ImageField(upload_to='doctors', blank=True, null=True)

    def __str__(self):
        return f'Dr. {self.employee.user.get_full_name()} - {self.department.name}'

class Nurse(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    nurse_image = models.ImageField(upload_to='nurses', blank=True, null=True)

    def __str__(self):
        return f'Nurse {self.employee.user.get_full_name()}'

class Receptionist(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    receptionist_image = models.ImageField(upload_to='receptionist', blank=True, null=True)

    def __str__(self):
        return f'Receptionist {self.employee.user.get_full_name()}'

class Availability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=9)  # E.g., 'Monday', 'Tuesday', etc.
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    class Meta:
        unique_together = ('doctor', 'day_of_week')  # Ensure one availability per day

    def __str__(self):
        return f'Dr. {self.doctor.employee.user.get_full_name()} - {self.doctor.department.name}'