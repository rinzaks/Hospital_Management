from django import forms
from .models import Appointment,MedicalHistory,Patient
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

   
class Login_Form(forms.Form):
    username = forms.CharField(
        max_length=10,
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Custom validation logic for password
        if len(password) < 6:  # Example check: password must be at least 6 characters
            raise forms.ValidationError("Password must be at least 6 characters long.")
        return password

class PatientForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = Patient
        fields = ['first_name','last_name','eid_num', 'mob_num', 'dob', 'gender', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control floating'}),  # Widget for the name field
            'last_name': forms.TextInput(attrs={'class': 'form-control floating'}),  # Widget for the name field
            'eid_num': forms.TextInput(attrs={'class': 'form-control floating'}),
            'mob_num': forms.TextInput(attrs={'class': 'form-control floating'}),  # Corrected this line
            'dob': forms.DateInput(attrs={'class': 'form-control floating', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control floating'}),
            'email': forms.EmailInput(attrs={'class': 'form-control floating'})  # Add this line for email field
        }

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['illness', 'surgeries', 'hospitalizations', 'family_medical_history']
        widgets = {
            'illness': forms.Textarea(attrs={'class': 'form-control'}),
            'surgeries': forms.Textarea(attrs={'class': 'form-control'}),
            'hospitalizations': forms.Textarea(attrs={'class': 'form-control'}),
            'family_medical_history': forms.Textarea(attrs={'class': 'form-control'}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'appointment_time']  # Exclude patient, email, mobile, and status
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'appointment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError("Your old password was entered incorrectly. Please enter it again.")
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields didn't match.")
        validate_password(password1, self.user)
        return password2

    def save(self):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        self.user.save()
        return self.user