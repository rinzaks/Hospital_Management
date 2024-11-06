# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Employee, Doctor, Nurse,Receptionist,Department,Availability,AdminProfile,CompanyLocation

class CompanyLocationForm(forms.ModelForm):
    class Meta:
        model = CompanyLocation
        fields = ['company_name', 'address', 'city', 'state', 'zip_code', 'country', 'phone_number']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'required': False}),
        }

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = AdminProfile
        fields = ['phone_number', 'address']
        widgets = {  # Use 'widgets' instead of 'widget'
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'})  # Use Textarea for multi-line input
        }

class AvailabilityForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        label='Select Doctor',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Availability
        fields = ['doctor', 'day_of_week', 'start_time', 'end_time']
        widgets = {
            'day_of_week': forms.Select(
                choices=[
                    ('Monday', 'Monday'),
                    ('Tuesday', 'Tuesday'),
                    ('Wednesday', 'Wednesday'),
                    ('Thursday', 'Thursday'),
                    ('Friday', 'Friday'),
                    ('Saturday', 'Saturday'),
                    ('Sunday', 'Sunday'),
                ],
                attrs={'class': 'form-control'}
            ),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

User = get_user_model()

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)  # Optional for edits

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:  # Only validate if email is provided
            if '@' not in email:
                raise forms.ValidationError("Please add '@' in the email address.")
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("This email is already taken.")
        return email

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_id', 'mobile_number', 'joining_date']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'joining_date': forms.DateInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Pop the user from kwargs to check permissions
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Make `employee_id` read-only for non-superusers
        if self.user and self.user.is_authenticated and not self.user.is_superuser:
            self.fields['employee_id'].widget.attrs['readonly'] = True  # Make the ID read-only for doctors (non-admins)
            self.fields['employee_id'].disabled = True  # Disable the field entirely (if you prefer it to be grayed out)

        # Make joining_date editable for superuser/admins only
        if self.user and not self.user.is_superuser:
            self.fields['joining_date'].widget.attrs['readonly'] = True  # Make it read-only for doctors and non-admins
            self.fields['joining_date'].disabled = True  # Disable field to prevent editing

    def clean_employee_id(self):
        employee_id = self.cleaned_data.get('employee_id')
        # Get the current employee instance (if we're editing an existing employee)
        employee_instance = self.instance  # The current employee object being edited
        
        # Check if employee_id has changed
        if employee_instance and employee_instance.employee_id != employee_id:
            if Employee.objects.filter(employee_id=employee_id).exists():
                raise forms.ValidationError("This Employee ID is already taken.")
        
        return employee_id

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['department', 'doc_image']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'doc_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class NurseForm(forms.ModelForm):
    class Meta:
        model = Nurse
        fields = ['nurse_image']
        widgets = {
            'nurse_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class ReceptionistForm(forms.ModelForm):
    class Meta:
        model = Receptionist
        fields = ['receptionist_image']
        widgets = {
            'accountant_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description', 'status', 'dep_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'cols': 30, 'rows': 4}),
            'status': forms.RadioSelect(),
            'dep_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'})  # Use file input
        }

class Staff_LoginForm(forms.Form):
    username = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password'}),required=True)
