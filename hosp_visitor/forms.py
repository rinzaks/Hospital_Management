from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from hosp_user.models import Patient
import re

class contactform(forms.Form):
    name = forms.CharField(
        max_length=25,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Name',
            'class': 'form-control',  # Bootstrap class for styling
            'id': 'name'
        })
    )
    email = forms.EmailField(
        max_length=25,
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your Email',
            'class': 'form-control',
            'id': 'email'
        })
    )
    subject = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Subject',
            'class': 'form-control',
            'id': 'subject'
        })
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'Leave a message here',
            'rows': 4,
            'class': 'form-control',
            'id': 'message'
        })
    )
   
class Registration(UserCreationForm):
    first_name = forms.CharField(required=True, label='First Name', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, label='Last Name', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(required=True, label='Username', max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    eid_num = forms.CharField(required=True, label='EID Number', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mob_num = forms.CharField(required=True, label='Mobile Number', max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, label="Email Address", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    gender = forms.CharField(required=True, label='Gender', max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dob = forms.DateField(required=True, label='Date of Birth', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    password1 = forms.CharField(required=True, label='Password', max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(required=True, label='Confirm Password', max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'eid_num', 'mob_num', 'password1', 'password2']

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError('Password should be at least 8 characters long')
        if not re.search(r'[a-z]', password1):
            raise forms.ValidationError('Password should have at least 1 lowercase letter')
        if not re.search(r'[A-Z]', password1):
            raise forms.ValidationError('Password should have at least 1 uppercase letter')
        if not re.search(r'[0-9]', password1):
            raise forms.ValidationError('Password should have at least 1 number')
        if not re.search(r'[!,@,#,$,%,&]', password1):
            raise forms.ValidationError('Password should have at least 1 special character')
        return password1
    def clean_eid_num(self):
        eid_num = self.cleaned_data.get('eid_num')
        if eid_num and Patient.objects.filter(eid_num=eid_num).exists():
            raise forms.ValidationError('A user with this EID Number already exists.')
        return eid_num

    def clean_mob_num(self):
        mob_num = self.cleaned_data.get('mob_num')
        if mob_num and Patient.objects.filter(mob_num=mob_num).exists():
            raise forms.ValidationError('A user with this Mobile Number already exists.')
        return mob_num

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Patient.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this Email Address already exists.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match')
        return cleaned_data
 