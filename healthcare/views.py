from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.db import connection

def main_page(request):
    return render(request, 'main_page.html')


def doctor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if authenticate_user('doctors', username, password):
            return HttpResponse("Welcome, Doctor!")
        else:
            return HttpResponse("Invalid doctor credentials")
    return render(request, 'doctor_login.html')



def clinic_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_data = authenticate_user('clinics1', username, password)
        if user_data:
            
            request.session['username'] = username
            return redirect('clinic_dashboard')
        else:
            return HttpResponse("Invalid patient credentials")
    return render(request, 'clinic_login.html')

def register_patient(request):
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')

        with connection.cursor() as cursor:
            query = """
                INSERT INTO patients (username, password, email, first_name, last_name, date_of_birth, gender, phone_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, [username, password, email, first_name, last_name, date_of_birth, gender, phone_number])
        
        return HttpResponse("Registration successful! Please login.")
    
    return redirect('patient_login')

def register_doctor(request):
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        specialization = request.POST.get('specialization')
        education = request.POST.get('education')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')

        # Store the doctor's details in the database
        with connection.cursor() as cursor:
            query = """
                INSERT INTO doctors (username, password, email, first_name, last_name, specialization, education, date_of_birth, gender, phone_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, [username, password, email, first_name, last_name, specialization, education, date_of_birth, gender, phone_number])

        return HttpResponse("Registration successful! Please login.")
    
    return redirect('doctor_login')

def register_clinic(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        clinic_name = request.POST.get('clinic_name')
        location = request.POST.get('location')
        specialization = request.POST.get('specialization')
        phone_number = request.POST.get('phone_number')

        with connection.cursor() as cursor:
            query = """
                INSERT INTO clinics1 (username, password, email, clinic_name, location, specialization, phone_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, [username, password, email, clinic_name, location, specialization, phone_number])

        return HttpResponse("Clinic registration successful! Please login.")
    
    return redirect('clinic_login')


def authenticate_user(table_name, username, password):
    with connection.cursor() as cursor:
        query = f"SELECT * FROM {table_name} WHERE username = %s AND password = %s"
        cursor.execute(query, [username, password])
        row = cursor.fetchone()
    return row  

# Patient login 
def patient_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_data = authenticate_user('patients', username, password)
        if user_data:

            request.session['username'] = username
            return redirect('patient_dashboard')
        else:
            return HttpResponse("Invalid patient credentials")
    return render(request, 'patient_login.html')

def doctor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_data = authenticate_user('doctors', username, password)
        if user_data:
            
            request.session['username'] = username
            return redirect('doctor_dashboard')
        else:
            return HttpResponse("Invalid patient credentials")
    return render(request, 'doctor_login.html')

def doctor_dashboard(request):
    
    username = request.session.get('username')
    if not username:
        return redirect('doctor_login')  
    with connection.cursor() as cursor:
        query = """
            SELECT first_name, last_name
            FROM doctors
            WHERE username = %s
        """
        cursor.execute(query, [username])
        row = cursor.fetchone()


    doctor_data = {}
    if row:
        doctor_data = {
            'first_name': row[0],
            'last_name': row[1],
        }

    context = {'doctor_data': doctor_data}
    return render(request, 'doctor_dashboard.html', context)



from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

# Fetch patients, doctors, and appointments
def fetch_patients(request):
    with connection.cursor() as cursor:
        query = "SELECT first_name, last_name, email,gender, phone_number FROM patients"
        cursor.execute(query)
        patients = cursor.fetchall()

    return patients

def fetch_doctors(request):
    with connection.cursor() as cursor:
        query = "SELECT first_name, last_name, specialization FROM doctors"
        cursor.execute(query)
        doctors = cursor.fetchall()

    return doctors

def fetch_appointments(request):
    with connection.cursor() as cursor:
        query = """
            SELECT name, appointment_date,time_slot,doctor_id, reason_for_visit
            FROM appointments1
        """
        cursor.execute(query)
        appointments = cursor.fetchall()

    return appointments

def clinic_dashboard(request):
    patients = fetch_patients(request)
    doctors = fetch_doctors(request)
    appointments = fetch_appointments(request)

    context = {
        'patients': patients,
        'doctors': doctors,
        'appointments': appointments,
    }

    return render(request, 'clinic_dashboard.html', context)


# Patient dashboard
def patient_dashboard(request):
    username = request.session.get('username')  
    if not username:
        return redirect('patient_login')

    # Fetch patient details from the database
    with connection.cursor() as cursor:
        query = """
            SELECT username, email, first_name, last_name, date_of_birth, gender, phone_number
            FROM patients
            WHERE username = %s
        """
        cursor.execute(query, [username])
        row = cursor.fetchone()

    # Map the row data to a dictionary
    profile_data = {}
    if row:
        profile_data = {
            'username': row[0],
            'email': row[1],
            'first_name': row[2],
            'last_name': row[3],
            'date_of_birth': row[4],
            'gender': row[5],
            'phone_number': row[6],
        }

    context = {'profile_data': profile_data}
    return render(request, 'patient_dashboard.html', context)

from django.views.decorators.csrf import csrf_exempt
# API to schedule an appointment
@csrf_exempt  # Decorator to allow POST requests 
def schedule_appointment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        doctor_id = request.POST.get('doctor_id')
        clinic_username = request.POST.get('clinic_username')
        appointment_date = request.POST.get('appointment_date')
        time_slot = request.POST.get('time_slot')
        reason_for_visit = request.POST.get('reason_for_visit')

        with connection.cursor() as cursor:
            query = """
                INSERT INTO appointments1 (name, doctor_id, clinic_username, appointment_date, time_slot, reason_for_visit)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, [name, doctor_id, clinic_username, appointment_date, time_slot, reason_for_visit])

        return HttpResponse("Appointment scheduled successfully", status=201)

    return HttpResponse("Invalid request method", status=400)

from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection


@csrf_exempt
def appointment_history(request):
    username = request.session.get('username')  
    if not username:
        return redirect('patient_login')  

    with connection.cursor() as cursor:
        query = """
            SELECT name, doctor_id, clinic_username, appointment_date, time_slot, reason_for_visit
            FROM appointments1
            WHERE LOWER(name) = LOWER(%s)
            ORDER BY appointment_date DESC
        """
        cursor.execute(query, [username])
        rows = cursor.fetchall()

    appointment_data = []
    for row in rows:
        appointment_data.append({
            'name': row[0],
            'doctor_id': row[1],
            'clinic_username': row[2],
            'appointment_date': row[3],
            'time_slot': row[4],
            'reason_for_visit': row[5],
        })

    return JsonResponse({'appointments': appointment_data})




from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout

def logout_view(request):
    auth_logout(request)
    return redirect('patient_login')


