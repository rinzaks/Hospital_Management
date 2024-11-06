from django.shortcuts import render,redirect,get_object_or_404
from .models import Patient,Appointment,MedicalHistory
from hosp_staff.models import Doctor,Department,Availability
from django.contrib import messages
from datetime import datetime, timedelta
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import PasswordChangeForm,PatientForm,MedicalHistoryForm,Login_Form,AppointmentForm
from django.utils import timezone
import uuid

@login_required(login_url='/404/')
def patient_add_appointment(request):
    doctors = Doctor.objects.all()
    departments = Department.objects.all()
    appointment_form = AppointmentForm()
    patient_form = PatientForm()

    if request.method == 'POST':
        appointment_form = AppointmentForm(request.POST)

        if appointment_form.is_valid():
            appointment = appointment_form.save(commit=False)
            try:
                patient = Patient.objects.get(user=request.user)
                appointment.patient = patient  # Assign the Patient instance
            except Patient.DoesNotExist:
                messages.error(request, "You are not registered as a patient. Please register first.")
                return redirect('create_patient')  # Redirect to patient registration

            appointment.status = 'scheduled'
            appointment.appointment_id = f"APT-{uuid.uuid4().hex[:8].upper()}"
            appointment.appointment_date = appointment_form.cleaned_data['appointment_date']
            appointment.appointment_time = appointment_form.cleaned_data['appointment_time']
            
            # Check doctor's availability
            day_of_week = appointment.appointment_date.strftime('%A')
            try:
                availability = Availability.objects.get(doctor=appointment.doctor, day_of_week=day_of_week)
            except Availability.DoesNotExist:
                messages.error(request, "The selected doctor is not available on that date.")
                return redirect('patient_add_appointment')

            if not (availability.start_time <= appointment.appointment_time <= availability.end_time):
                messages.error(request, "The selected time is outside the doctor's available hours.")
                return redirect('patient_add_appointment')

            existing_appointments = Appointment.objects.filter(
                doctor=appointment.doctor,
                appointment_date=appointment.appointment_date
            )

            for existing in existing_appointments:
                existing_time = datetime.combine(appointment.appointment_date, existing.appointment_time)
                requested_time = datetime.combine(appointment.appointment_date, appointment.appointment_time)
                
                if abs((existing_time - requested_time).total_seconds()) < 900:  # 15 minutes
                    messages.error(request, "The selected time slot is already taken.")
                    return redirect('patient_home')

            appointment.save()
            messages.success(request, "Appointment scheduled successfully!")
            return redirect('my_appointments')
        else:
            messages.error(request, 'Appointment failed. Please check the appointment form.')

    return render(request, 'hosp_user/patient_add_appointment.html', {
        'appointment_form': appointment_form,
        'doctors': doctors,
        'departments': departments,
        'patient_form': patient_form,
        'patient': request.user,
    })

@login_required(login_url='/404/')
def my_appointments(request):
    patient = Patient.objects.get(user=request.user)
    appointments = Appointment.objects.filter(patient=patient)
    now = timezone.now()      
    completed_appointments = appointments.filter(appointment_date__lt=now, status='completed')
    scheduled_appointments = appointments.filter(appointment_date__gte=now, status='scheduled')
    canceled_appointments = appointments.filter(status='canceled')
    return render(request, 'hosp_user/my_appointments.html', {
        'completed_appointments': completed_appointments,
        'scheduled_appointments': scheduled_appointments,
        'canceled_appointments': canceled_appointments,
        'appointments': appointments,
        'patient': patient,
    })

@login_required(login_url='/404/')
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    doctors = Doctor.objects.all()
    departments = Department.objects.all()
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()  # Save the updated appointment
            messages.success(request, "Appointment updated successfully!")
            return redirect('my_appointments')
    else:
        form = AppointmentForm(instance=appointment)  # Pre-populate the form with current appointment data

    return render(request, 'hosp_user/edit_appointment.html', {
        'form': form,
        'doctors': doctors,
        'departments': departments,
        'appointment': appointment,  # Pass the current appointment for context
    })

@login_required(login_url='/404/')
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if appointment.patient.user == request.user:
        appointment.delete()  # Delete the appointment
        messages.success(request, "Appointment deleted successfully!")
    return redirect('my_appointments')

@login_required(login_url='/404/')
def schedule_view(request):
    doctor = Doctor.objects.all()
    availability = Availability.objects.all()
    return render(request, 'hosp_user/availability_user.html', {'availability': availability, 'doctor' : doctor})

@login_required(login_url='/404/')
def delete_appointment(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = 'canceled'  # Update status to canceled
        appointment.save()
        messages.success(request, "Appointment has been canceled successfully.")
    except Appointment.DoesNotExist:
        messages.error(request, "Appointment not found.")
    
    return redirect('my_appointments')  # Redirect back to the appointments page


@login_required(login_url='/404/')
def edit_myprofile(request):
    patient = get_object_or_404(Patient, user=request.user)
    medical_history, created = MedicalHistory.objects.get_or_create(patient=patient)
    if request.method == 'POST':
        patient_form = PatientForm(request.POST, instance=patient)
        medical_history_form = MedicalHistoryForm(request.POST, instance=medical_history)
        if patient_form.is_valid() and medical_history_form.is_valid():
            patient_form.save()
            medical_history_form.save()
            messages.success(request, 'Profile and Medical History updated successfully!')
            return redirect('patient_home')  # Redirect to patient's home or another page
    else:
        patient_form = PatientForm(instance=patient)
        medical_history_form = MedicalHistoryForm(instance=medical_history)

    # Return the response with both forms in the context
    return render(request, 'hosp_user/edit_myprofile.html', {
        'patient_form': patient_form,
        'medical_history_form': medical_history_form,
        'patient': patient,
    })

def login_patient(request):
    if request.method == 'POST':
        form = Login_Form(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {user.get_full_name()}!')
                return redirect('patient_home')                
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = Login_Form()
    return render(request, 'hosp_user/login.html', {'form': form})

@login_required(login_url='/404/')
def delete_profile(request):
    user = request.user
    try:
        patient = Patient.objects.get(user=user)
    except Patient.DoesNotExist:
        messages.error(request, "Patient profile does not exist.")
        return redirect('home')  # Redirect to home if no profile exists

    if request.method == 'POST':
        # Delete the patient profile
        patient.delete()
        messages.success(request, "Your profile has been deleted successfully.")
        return redirect('home')  # Redirect to a page after deletion

    return render(request, 'hosp_user/delete_profile.html', {'patient': patient})

@login_required(login_url='/404/')
def patient_home(request):
    patient = Patient.objects.get(user=request.user)
    medical_histories = MedicalHistory.objects.filter(patient=patient)
    appointments = Appointment.objects.filter(patient=patient)

    context = {
        'patient': patient,
        'medical_histories': medical_histories,
        'appointments': appointments,
    }

    return render(request, 'hosp_user/patient_home.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/404/')
def changepassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully.')
            return redirect('login_patient')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'hosp_user/changepassword.html', {'form': form})