from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout,get_user_model
from .models import Employee,Doctor,Department,Availability,AdminProfile,CompanyLocation
from hosp_user.forms import PasswordChangeForm
from .forms import EmployeeForm,CompanyLocationForm,Staff_LoginForm,AdminProfileForm,DepartmentForm,AvailabilityForm,UserForm,EmployeeForm, DoctorForm, NurseForm, ReceptionistForm
from hosp_user.models import Appointment,Patient,MedicalHistory
from hosp_user.forms import PatientForm,MedicalHistoryForm,AppointmentForm
from django.contrib.auth.decorators import login_required
import uuid
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import Group


#__________-Appointments__________
@login_required(login_url='/404/')
def admin_receptionist_add_appointment(request):
    doctors = Doctor.objects.all()
    departments = Department.objects.all()
    appointment_form = AppointmentForm()
    patient_form = PatientForm()

    if request.method == 'POST':
        patient_form = PatientForm(request.POST)

        if patient_form.is_valid():
            username = patient_form.cleaned_data['username']
            eid_num = patient_form.cleaned_data['eid_num']

            # Check if the patient already exists
            try:
                patient = Patient.objects.get(eid_num=eid_num)
                messages.info(request, "Patient found. Proceeding to schedule appointment.")
            except Patient.DoesNotExist:
                # Create a new User instance if the patient does not exist
                password = patient_form.cleaned_data.get('password')
                user = User.objects.create_user(username=username, password=password)
                user.first_name = patient_form.cleaned_data['first_name']  # Add this
                user.last_name = patient_form.cleaned_data['last_name']
                user.save()

                # Create the Patient instance
                patient = patient_form.save(commit=False)
                patient.user = user  # Link user to patient
                patient.save()
                messages.success(request, "New patient created successfully!")

            # Now handle the appointment form
            appointment_form = AppointmentForm(request.POST)
            if appointment_form.is_valid():
                appointment = appointment_form.save(commit=False)
                appointment.patient = patient  # Assign the Patient instance
                appointment.status = 'scheduled'
                appointment.appointment_id = f"APT-{uuid.uuid4().hex[:8].upper()}"
                # Add additional appointment logic here...

                appointment.save()
                messages.success(request, "Appointment scheduled successfully!")

                return redirect('all_appointments')  # Redirect after successful appointment creation

    # Determine the appropriate template to render
    if request.user.is_superuser:
        template_name = 'hosp_staff/admin_add_appointment.html'
    elif hasattr(request.user, 'employee') and hasattr(request.user.employee, 'receptionist'):
        template_name = 'hosp_staff/recep_add_appointment.html'
    else:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')

    # Render the appropriate template with patient information
    context = {
        'appointment_form': appointment_form,
        'doctors': doctors,
        'departments': departments,
        'patient_form': patient_form,
        'patient': patient if 'patient' in locals() else None,
    }
    
    return render(request, template_name, context)

@login_required(login_url='/404/')
def all_appointments(request):
    appointments = []  # Initialize an empty list for appointments
    template_name = ''  # Initialize template name

    if request.user.is_superuser:
        appointments = Appointment.objects.all().order_by('-appointment_date', '-appointment_time')  # Superuser sees all appointments
        template_name = 'hosp_staff/all_appointments.html'  # Template for superuser
    elif hasattr(request.user, 'employee') and hasattr(request.user.employee, 'doctor'):
        appointments = Appointment.objects.filter(doctor=request.user.employee.doctor).order_by('-appointment_date', '-appointment_time')  # Doctor sees their appointments
        template_name = 'hosp_staff/doc_appointments.html'  # Template for doctor
    elif hasattr(request.user, 'employee') and hasattr(request.user.employee, 'receptionist'):
        appointments = Appointment.objects.all().order_by('-appointment_date', '-appointment_time')  # Receptionist sees all appointments
        template_name = 'hosp_staff/recep_appointments.html'  # Template for receptionist
    else:
        messages.error(request, 'You do not have permission to view appointments.')  # Error message for unauthorized users

    # Update appointment statuses based on the current time
    current_time = timezone.now()  # Get the current time
    for appointment in appointments:
        if appointment.status == 'cancelled':
            continue  # Keep cancelled appointments as they are
        if appointment.appointment_date < current_time.date() or (
            appointment.appointment_date == current_time.date() and appointment.appointment_time < current_time.time()
        ):
            appointment.status = 'completed'
        else:
            appointment.status = 'scheduled'

    # Instead of returning 'appointments' directly, ensure the status is reflected in your template
    return render(request, template_name, {'appointments': appointments})

@login_required(login_url='/404/')
def edit_patient_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('all_appointments')  # Redirect to the appointments list
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'hosp_staff/edit__patient_appointment.html', {'form': form, 'appointment': appointment})

@login_required(login_url='/404/')
def patient_delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.delete()
        return redirect('all_appointments')  # Redirect to the appointments list
    return render(request, 'hosp_staff/delete_appointment.html', {'appointment': appointment})

#________Availability__________________

@login_required(login_url='/404/')
def all_schedules(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            availability = Availability.objects.all()
    return render(request, 'hosp_staff/all_schedules.html', {
        'availability': availability,
    })

@login_required(login_url='/404/')
def my_schedules(request):
    availability = []  # Initialize availability list

    if request.user.is_authenticated:
        if hasattr(request.user, 'doctor'):
            # Doctor sees their specific appointments
            availability = Availability.objects.filter(doctor=request.user.doctor)
        else:
            print("User does not have an expected role.")  # Handle case for other user types if needed

    # Render the schedule page with the appropriate availability data
    return render(request, 'hosp_staff/my_schedules.html', {
        'availability': availability,
    })

@login_required(login_url='/404/')
def my_patients(request):
    if hasattr(request.user, 'employee') and hasattr(request.user.employee, 'doctor'):
        patients = Patient.objects.all()
    #     doctor = request.user.employee.doctor
    #     appointments = Appointment.objects.filter(doctor=doctor)

    #     # Get the list of patients associated with this doctor through appointments
    #     patients = [appointment.patient for appointment in appointments]
    # else:
    #     patients = []  # No patients if the user is not a doctor

    return render(request, 'hosp_staff/my_patients.html', {
        'patients': patients,
    })



@login_required(login_url='/404/')
def add_availability(request):
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('all_schedules')  # Redirect to a page where superusers can manage availability
    
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        
        if form.is_valid():
            availability = form.save()
            messages.success(request, 'Availability added successfully!')
            return redirect('all_schedules')  # Redirect to availability management page
        else:
            # If form is not valid, show errors
            messages.error(request, 'There was an error with the form. Please check the details and try again.')
    else:
        # For GET requests, show an empty form
        form = AvailabilityForm()
    
    # Pass form to the template
    return render(request, 'hosp_staff/add_availability.html', {'form': form},)


@login_required(login_url='/404/')
def edit_availability(request, availability_id):
    availability = get_object_or_404(Availability, id=availability_id)

    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('all_schedules')  # Redirect to an appropriate page

    if request.method == 'POST':
        form = AvailabilityForm(request.POST, instance=availability)
        if form.is_valid():
            form.save()
            messages.success(request, 'Availability updated successfully!')
            return redirect('all_schedules')
    else:  # Handle GET request
        form = AvailabilityForm(instance=availability)

    return render(request, 'hosp_staff/edit_availability.html', {
        'form': form,
        'availability': availability,
    })

@login_required(login_url='/404/')
def delete_availability(request, availability_id):
    availability = get_object_or_404(Availability, id=availability_id)

    if request.user.is_superuser:
        if request.method == 'POST':
            availability.delete()
            messages.success(request, 'Availability deleted successfully!')
            return redirect('all_schedules')  # Redirect after deletion
    else:
        messages.success(request, 'You are not authorized to do this !!')
    return render(request, 'hosp_staff/delete_availability.html', {
        'availability': availability,
    })
#________Department_________________

@login_required(login_url='/404/')
def departments(request):
    dep = Department.objects.all()
    return render(request,'hosp_staff/departments.html',{'dep':dep})

@login_required(login_url='/404/')
def create_department(request):
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('departments')  # Redirect to a suitable page

    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully.')
            return redirect('departments')  # Redirect to a suitable page
    else:
        form = DepartmentForm()
    
    return render(request, 'hosp_staff/add_department.html', {'form': form})

@login_required(login_url='/404/')
def edit_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('departments')  # Redirect to the departments list page

    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully.')
            return redirect('departments')  # Redirect to the departments list page
    else:
        form = DepartmentForm(instance=department)
    
    return render(request, 'hosp_staff/edit_department.html', {'form': form, 'department': department})

@login_required(login_url='/404/')
def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)

    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('departments')  # Redirect to the departments list page

    # Handle the deletion only for POST requests
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department deleted successfully.')
        return redirect('departments')  # Redirect back to the departments list

    # If not a POST request, redirect back to departments
    return redirect('departments')

#________Employees__________________

@login_required(login_url='/404/')
def staff_selection(request):
    return render(request, 'hosp_staff/staff_selection.html')

@login_required(login_url='/404/')
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    # Check if the user is a superuser
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('employees')  # Redirect to the employee list

    # Initialize forms
    employee_form = EmployeeForm(instance=employee)
    user_form = UserForm(instance=employee.user)  # Ensure user_form is always defined

    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST, instance=employee)
        user_form = UserForm(request.POST, instance=employee.user)

        # Initialize staff-specific form based on the employee's type
        staff_form = None
        if hasattr(employee, 'doctor'):
            staff_form = DoctorForm(request.POST, request.FILES, instance=employee.doctor)
        elif hasattr(employee, 'nurse'):
            staff_form = NurseForm(request.POST, request.FILES, instance=employee.nurse)
        elif hasattr(employee, 'receptionist'):
            staff_form = ReceptionistForm(request.POST, request.FILES, instance=employee.receptionist)
        
        if employee_form.is_valid() and user_form.is_valid() and (staff_form is None or staff_form.is_valid()):
            employee_form.save()  # Save the Employee form
            user_form.save()  # Save the User form
            if staff_form:  # Only save the staff form if it exists
                staff_form.save()
            messages.success(request, 'Employee updated successfully!')
            return redirect('employees')  # Adjust this to your employee list URL

    # If not POST, the forms are already initialized above

    context = {
        'employee_form': employee_form,
        'user_form': user_form,
        'employee': employee,
    }

    return render(request, 'hosp_staff/edit_employee.html', context)

@login_required(login_url='/404/')
def view_employee(request, employee_id):
    if request.user.is_superuser or request.user.is_staff:
        employee = get_object_or_404(Employee, id=employee_id)
    context = {
        'employee': employee,
    }

    return render(request, 'hosp_staff/view_employee.html', context)

@login_required(login_url='/404/')
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    # Check if the user is a superuser
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('employees')  # Redirect to the employee list

    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted successfully!')
        return redirect('employees')  # Replace with your employee list URL

    return render(request, 'hosp_staff/delete_employee.html', {'employee': employee})

User = get_user_model()

@login_required(login_url='/404/')
def create_staff(request, staff_type):
    user_form = UserForm()
    employee_form = EmployeeForm()
    staff_form = None  # Initialize staff_form to None

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        employee_form = EmployeeForm(request.POST)

        if user_form.is_valid() and employee_form.is_valid():
            # Create the user account
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Create the employee record
            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()

            # Handle staff-specific forms
            if staff_type == 'doctor':
                staff_form = DoctorForm(request.POST, request.FILES)
            elif staff_type == 'nurse':
                staff_form = NurseForm(request.POST, request.FILES)
            elif staff_type == 'receptionist':
                staff_form = ReceptionistForm(request.POST, request.FILES)

            if staff_form and staff_form.is_valid():
                staff_member = staff_form.save(commit=False)
                staff_member.employee = employee
                staff_member.save()

            messages.success(request, f"{user.get_full_name()} has been added successfully.")
            return redirect('employees')  # Redirect to the employees list

    else:
        # Initialize forms for GET request
        if staff_type == 'doctor':
            staff_form = DoctorForm()
        elif staff_type == 'nurse':
            staff_form = NurseForm()
        elif staff_type == 'receptionist':
            staff_form = ReceptionistForm()

    context = {
        'user_form': user_form,
        'employee_form': employee_form,
        'staff_type': staff_type,
        'staff_form': staff_form,
    }

    return render(request, 'hosp_staff/add_employee.html', context)


@login_required(login_url='/404/')
def employees(request):
    # Check if the user is staff
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('home')  # Redirect to a suitable page (e.g., home)

    employees = Employee.objects.all()
    return render(request, 'hosp_staff/employees.html', {'employees': employees})

@login_required(login_url='/404/')
def doctors_list(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('home')  # Redirect to a suitable page (e.g., home)

    doctors = Doctor.objects.all()
    context = {
        'doctors': doctors,
    }
    return render(request, 'hosp_staff/doctors_list.html', context)

@login_required(login_url='/404/')
def patients_list(request):
    # Check if the user is a superuser
    if request.user.is_superuser:
        patients = Patient.objects.all()  # Superuser sees all patients
        context = {
            'patients': patients,
        }
        return render(request, 'hosp_staff/patients_list.html', context)

    # Check if the user is a receptionist
    elif hasattr(request.user, 'employee') and hasattr(request.user.employee, 'receptionist'):
        receptionist = request.user.employee.receptionist
        patients = Patient.objects.all()  # Receptionist sees all patients
        context = {
            'patients': patients,
            'receptionist':receptionist,
        }
        return render(request, 'hosp_staff/recep_patients_list.html', context)

    # Check if the user is a doctor
    elif hasattr(request.user, 'doctor'):
        doctor = request.user.doctor
        patients = Patient.objects.filter(user=request.user)  # Fetch patients assigned to this doctor
        context = {
            'patients': patients,
            'doctor':doctor,
        }
        return render(request, 'hosp_staff/my_patients.html', context)

    # If user is not authorized, redirect to home
    return redirect('home')

#----------------Admin____________
User = get_user_model()
try:
    user = User.objects.get(username='admin_medicare')
    AdminProfile.objects.get_or_create(user=user)  # Use get_or_create to avoid duplicates
except User.DoesNotExist:
    # Handle the case where the user does not exist
    print("Admin user not found.")

@login_required(login_url='/404/')
def edit_admin_profile(request):
    admin_profile = get_object_or_404(AdminProfile, user=request.user)

    if request.method == 'POST':
        # Use the existing admin profile instance to update
        form = AdminProfileForm(request.POST, request.FILES, instance=admin_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('admin_dashboard')  # Redirect to admin dashboard or desired page
    else:
        # For GET request, load the current admin profile data
        form = AdminProfileForm(instance=admin_profile)

    return render(request, 'hosp_staff/edit_admin_profile.html', {'form': form})


@login_required(login_url='/404/')
def edit_my_profile(request):
    employee = get_object_or_404(Employee, user=request.user)

    # Initialize the forms based on the employee type
    staff_form = EmployeeForm(request.POST or None, instance=employee, user=request.user)

    # Handle doctor-specific form
    if hasattr(employee, 'doctor'):
        specific_form = DoctorForm(request.POST or None, instance=employee.doctor)
        template_name = 'hosp_staff/doc_edit_my_profile.html'  # Template for doctor
    else:
        specific_form = None
        template_name = 'hosp_staff/edit_my_profile.html'  # Default template for other staff

    if request.method == 'POST':
        if staff_form.is_valid() and (specific_form is None or specific_form.is_valid()):
            staff_form.save()
            if specific_form:
                specific_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('doctor_dashboard')  # Redirect to the dashboard for the specific employee type

    context = {
        'staff_form': staff_form,
        'specific_form': specific_form,
    }

    return render(request, template_name, context)

@login_required(login_url='/404/')
def admin_dashboard(request):
    context = {}

    if request.user.is_superuser:
        # Retrieve all records
        patients = Patient.objects.all()
        employees = Employee.objects.all()
        department = Department.objects.all()
        all_appointments = Appointment.objects.all()
        doctors = Doctor.objects.all()
        summary_doctors = doctors[:4]
        employee_counts = {
            'Doctor': 0,
            'Receptionist': 0,
            'Nurse': 0,
        }

        # Count the number of employees by type
        for emp in employees:
            staff_type = emp.get_staff_type()
            if staff_type in employee_counts:
                employee_counts[staff_type] += 1
        # Get total counts
        total_patients = patients.count()
        total_employees = employees.count()
        total_appointments = all_appointments.count()
        total_doctors = doctors.count()
        # Add data to context
        context = {
            'patients': patients,
            'department': department,
            'doctors': doctors,
            'total_patients': total_patients,
            'total_employees': total_employees,
            'employee_counts': employee_counts,
            'total_appointments': total_appointments,
            'all_appointments': all_appointments,
            'total_doctors': total_doctors,
            'summary_doctors': summary_doctors,
            'graph_image': '/media/graphs/line_graph.png',  # Path to the graph image
        }

    return render(request, 'hosp_staff/admin_dashboard.html', context)

@login_required(login_url='/404/')
def view_myprofile(request):
    admin_profile = AdminProfile.objects.get(user=request.user)
    context = {
        'admin_profile': admin_profile,
    }
    return render(request,'hosp_staff/view_myprofile.html', context)

@login_required(login_url='/404/')
def staff_logout(request):
    logout(request)  # Log out the user
    messages.success(request, "You have been logged out successfully.")
    return redirect('staff_login')

@login_required(login_url='/404/')
def reset_password(request):
    # Initialize template_name in case of missing conditions
    template_name = 'hosp_staff/reset_password.html'  # Default template for superuser

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully.')
            return redirect('staff_login')
    else:
        form = PasswordChangeForm(request.user)

    # Determine the appropriate template based on the user's role
    if request.user.is_superuser:
        template_name = 'hosp_staff/reset_password.html'  # Template for superuser

    elif hasattr(request.user, 'employee'):
        if hasattr(request.user.employee, 'doctor'):
            template_name = 'hosp_staff/reset_doc_password.html'  # Template for doctors
        elif hasattr(request.user.employee, 'receptionist'):
            template_name = 'hosp_staff/reset_recep_password.html'  # Template for receptionists
        else:
            messages.error(request, "You do not have permission to access this page.")
            return redirect('staff_login')

    return render(request, template_name, {'form': form})

def staff_login(request):
    if request.method == 'POST':
        form = Staff_LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_staff:
                login(request, user)

                if user.is_superuser:  # Check if the user is an admin
                    return redirect('admin_dashboard')  # Redirect to admin dashboard
                elif user.groups.filter(name='Doctors').exists():
                    return redirect('doctor_dashboard') 
                elif user.groups.filter(name='Nurse').exists():
                    return redirect('receptionist_dashboard') 
                elif user.groups.filter(name='Receptionist').exists():
                    return redirect('receptionist_dashboard')  
                else:
                    return redirect('home') 
    else:
        form = Staff_LoginForm()

    return render(request, 'hosp_staff/staff_login.html', {'form': form})

@login_required(login_url='/404/')
def doctor_dashboard(request):
    employee = request.user.employee  # Access the Employee instance through the User
    doctor = employee.doctor
    doctor_name = doctor.employee.user.get_full_name()  # Access the user's full name
    context = {
        'doctor': doctor,
        'doctor_name': doctor_name,  # Include the doctor's name in the context
    }

    return render(request, 'hosp_staff/doctor_dashboard.html', context)

@login_required(login_url='/404/')
def nurse_dashboard(request):
    employee = request.user.employee  # Access the Employee instance through the User
    nurse = employee.nurse  # Access the Nurse instance if exists
    nurse_name = nurse.employee.user.get_full_name()  # Get nurse's full name
    context = {
            'nurse': nurse,
            'nurse_name': nurse_name,
        }
    return render(request, 'hosp_staff/nurse_dashboard.html',context)

@login_required(login_url='/404/')
def receptionist_dashboard(request):
    employee = request.user.employee  # Access the Employee instance through the User
    receptionist = employee.receptionist  # Access the Receptionist instance if exists
    receptionist_name = receptionist.employee.user.get_full_name() 
    patients = Patient.objects.all()
     # Get receptionist's full name
    context = {
            'receptionist': receptionist,
            'receptionist_name': receptionist_name,
            'patients': patients,
        }
    return render(request, 'hosp_staff/receptionist_dashboard.html',context)

@login_required(login_url='/404/')
def view_my_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    medical_histories = patient.medical_histories.all()  # Get all medical histories related to the patient
    return render(request, 'hosp_staff/view_my_patient.html', {
        'patient': patient,
        'medical_histories': medical_histories,
    })

@login_required(login_url='/404/') 
def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    # Check if the user is a superuser
    if request.user.is_superuser:
        if request.method == 'POST':
            form = PatientForm(request.POST, instance=patient)
            if form.is_valid():
                form.save()
                messages.success(request, 'Patient updated successfully!')
                return redirect('patients_list')
        else:
            form = PatientForm(instance=patient)

        return render(request, 'hosp_staff/edit_patient.html', {
            'form': form,
            'patient': patient,
        })
    else:
        messages.error(request, 'You are not authorized to edit this patient.')
        return redirect('patients_list')

@login_required(login_url='/404/') 
def doc_edit_patient(request, patient_id):
    if hasattr(request.user, 'employee') and hasattr(request.user.employee, 'doctor'):
        # Get the patient by ID
        patient = get_object_or_404(Patient, id=patient_id)
        medical_histories = MedicalHistory.objects.filter(patient=patient)

        if request.method == 'POST':
            form = PatientForm(request.POST, instance=patient)
            medical_history_form = MedicalHistoryForm(request.POST)  # No instance for new entry

            if form.is_valid() and medical_history_form.is_valid():
                # Save patient data
                form.save()
                
                # Save new medical history data
                medical_history = medical_history_form.save(commit=False)
                medical_history.patient = patient  # Associate with the patient
                medical_history.save()

                messages.success(request, 'Patient profile and medical history updated successfully!')
                return redirect('view_my_patient', patient_id=patient.id)
        else:
            form = PatientForm(instance=patient)
            medical_history_form = MedicalHistoryForm()  # Create an empty form for new entry

        return render(request, 'hosp_staff/doc_edit_patient.html', {
            'form': form,
            'patient': patient,
            'medical_histories': medical_histories,
            'medical_history_form': medical_history_form,  # Include the new form in the context
        })

    # If the user is not a doctor, redirect or show an error
    return redirect('home')


@login_required(login_url='/404/')
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.user.is_superuser:
        if request.method == 'POST':
            # Soft delete the patient profile
            patient.is_active = False
            patient.deleted_at = timezone.now()
            patient.save()

            messages.success(request, 'Patient marked as deleted successfully!')
            return redirect('patients_list')  # Redirect to a list of patients or another page

        # If the request method is GET, render the delete confirmation page
        return render(request, 'hosp_staff/delete_patient.html', {
            'patient': patient,
        })
    
    messages.error(request, 'You do not have permission to delete this patient.')
    return redirect('patients_list')

@login_required(login_url='/404/')
def create_company_location(request):
    if request.user.is_superuser:  # Adjust the role check as necessary
        if request.method == 'POST':
            form = CompanyLocationForm(request.POST)
            if form.is_valid():
                # Save the form and get the instance of the saved company location
                company_location = form.save()
                messages.success(request, 'Company details updated successfully!')
                return redirect('create_company_location')  # Redirect to the same page to show updated data
        else:
            form = CompanyLocationForm()

        # In GET request, we pass the existing company details (if any)
        company_location = CompanyLocation.objects.first()  # Get the first company location, or adjust to your needs

        return render(request, 'hosp_staff/company_info.html', {'form': form, 'company_location': company_location})

@login_required(login_url='/404/')
def create_patient(request):
    # Handle patient creation for doctors
    if hasattr(request.user, 'employee') and hasattr(request.user.employee, 'doctor'):
        doctor = request.user.employee.doctor
        
        # Check if the request method is POST (form submission)
        if request.method == 'POST':
            # Create form instances with the posted data
            patient_form = PatientForm(request.POST)
            medical_history_form = MedicalHistoryForm(request.POST)

            # Check if both forms are valid
            if patient_form.is_valid() and medical_history_form.is_valid():
                # Create User instance manually
                username = patient_form.cleaned_data['username']
                password = patient_form.cleaned_data['password']
                first_name = patient_form.cleaned_data['first_name']
                last_name = patient_form.cleaned_data['last_name']
                email = patient_form.cleaned_data['email']

                # Create User object
                user = User.objects.create_user(username=username, password=password, email=email)
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                # Create patient instance but don't save yet (commit=False)
                patient = patient_form.save(commit=False)
                patient.user = user  # Assign the created User to the patient
                patient.save()  # Save the patient instance

                # Now save the medical history, associating it with the patient
                medical_history = medical_history_form.save(commit=False)
                medical_history.patient = patient
                medical_history.save()  # Save the medical history

                messages.success(request, 'Patient and Medical History created successfully!')
                return redirect('my_patients')  # Redirect to the doctor's list of patients

            else:
                # If forms are not valid, show error messages for each field
                for field in patient_form.errors:
                    messages.error(request, f"{field}: {patient_form.errors[field]}")
                for field in medical_history_form.errors:
                    messages.error(request, f"{field}: {medical_history_form.errors[field]}")

        else:
            # If the request is not a POST, instantiate empty forms
            patient_form = PatientForm()
            medical_history_form = MedicalHistoryForm()

        # Use a specific template for doctors
        return render(request, 'hosp_staff/doc_add_patient.html', {
            'patient_form': patient_form,
            'medical_history_form': medical_history_form,
        })

    # If the user is not a doctor, redirect
    else:
        messages.error(request, 'You do not have permission to create a patient.')
        return redirect('home')
