from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('patient-login/', views.patient_login, name='patient_login'),
    path('doctor-login/', views.doctor_login, name='doctor_login'),
    path('clinic-login/', views.clinic_login, name='clinic_login'),
    path('register_patient/', views.register_patient, name='register_patient'),
    path('register_doctor/', views.register_doctor, name='register_doctor'),
    path('register_clinic/', views.register_clinic, name='register_clinic'),  
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('schedule-appointment/', views.schedule_appointment, name='schedule_appointment'),
    
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('clinic_dashboard/', views.clinic_dashboard, name='clinic_dashboard'),
   

    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),

    path('appointment_history/', views.appointment_history, name='appointment_history'),
   
]