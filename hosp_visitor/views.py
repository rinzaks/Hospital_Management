from django.shortcuts import render,redirect
from hosp_staff.models import Department,Doctor,CompanyLocation
from hosp_user.models import Patient
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone  # Import timezone
from .forms import contactform,Registration
# from .tasks import send_query_email_task

def home(request):
    dep = Department.objects.all()
    loc = CompanyLocation.objects.all()
    doc = Doctor.objects.all()
    context = {
        'dep': dep,
        'doc': doc,
        'loc': loc,
    }
    return render(request,'hosp_visitor/home.html',context)

def about(request):
    dep = Department.objects.all()
    loc = CompanyLocation.objects.all()
    doc = Doctor.objects.all()
    context = {
        'dep': dep,
        'doc': doc,
        'loc': loc,
    }
    return render(request,'hosp_visitor/about.html',context)

def contact(request):
    dep = Department.objects.all()
    loc = CompanyLocation.objects.all()
    doc = Doctor.objects.all()
    context = {
        'dep': dep,
        'doc': doc,
        'loc': loc,
    }
    if request.method == 'POST':
        form = contactform(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            messages.success(request, "Query ")
            # send_query_email_task.delay(name, email, subject, message)
            return redirect('home')
    else:
        form = contactform()

    return render(request, 'hosp_visitor/contact.html', {'form': form},context)

def doctors(request):
    dep = Department.objects.all()
    loc = CompanyLocation.objects.all()
    doc = Doctor.objects.all()
    context = {
        'dep': dep,
        'doc': doc,
        'loc': loc,
    }
    return render(request,'hosp_visitor/doctors.html',context)

def services(request):
    dep = Department.objects.all()
    loc = CompanyLocation.objects.all()
    doc = Doctor.objects.all()
    context = {
        'dep': dep,
        'doc': doc,
        'loc': loc,
    }
    return render(request,'hosp_visitor/service.html',context)

def register(request):
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            user = form.save()
            Patient.objects.create(
                user=user,
                email=form.cleaned_data.get('email'),
                gender=form.cleaned_data.get('gender'),
                eid_num=form.cleaned_data.get('eid_num'),
                dob=form.cleaned_data.get('dob'),
                mob_num=form.cleaned_data.get('mob_num')
            )
            messages.success(request, "User successfully registered.")
            return redirect('login_patient')
    else:
        form = Registration()
    
    return render(request, 'hosp_user/register_user.html', {'form': form})

def custom_404_view(request, exception):
    return render(request, 'hosp_visitor/404.html', status=404)
