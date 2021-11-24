from .views import (
CustomAuthToken,
DoctorAccountViewAdmin,
DocRegistrationViewAdmin,
ApproveDoctorViewAdmin, 
AppointmentViewAdmin,
PetRegistrationViewAdmin,
PetAccountViewAdmin,
PetHistoryViewAdmin,
ApprovePetViewAdmin,
ApproveAppointmentViewAdmin,
)

from django.urls import path



app_name='clinicAdmin'
urlpatterns = [
    #Admin login
    path('login/', CustomAuthToken.as_view(), name='api_admin_login'),

 
    #Approve Doctor
    path('approve/doctors/', ApproveDoctorViewAdmin.as_view(), name='api_doctors_approve_admin'),
    path('approve/doctor/<uuid:pk>/', ApproveDoctorViewAdmin.as_view(), name='api_doctor_detail_approve_admin'),

    #Approve Patient
    path('approve/pets/', ApprovePetViewAdmin.as_view(), name='api_pets_approve_admin'),
    path('approve/pet/<uuid:pk>/', ApprovePetViewAdmin.as_view(), name='api_pet_detail_approve_admin'),

    # Approve Appointment
    path('approve/appointments/', ApproveAppointmentViewAdmin.as_view(), name='api_appointment_approve_admin'),
    path('approve/appointment/<int:pk>', ApproveAppointmentViewAdmin.as_view(), name='api_appointment_approve_detail_admin'),

    #Doctor management
    path('doctor/registration/', DocRegistrationViewAdmin.as_view(), name='api_doctors_registration_admin'),
    path('doctors/', DoctorAccountViewAdmin.as_view(), name='api_doctors_admin'),
    path('doctor/<uuid:pk>/', DoctorAccountViewAdmin.as_view(), name='api_doctor_detail_admin'),
    
    #Pet Management
    path('pet/registration/', PetRegistrationViewAdmin.as_view(), name='api_pet_registration_admin'),
    path('pets/', PetAccountViewAdmin.as_view(), name='api_pets_admin'),
    path('pet/<uuid:pk>/', PetAccountViewAdmin.as_view(), name='api_pet_detail_admin'),
    path('pet/<uuid:pk>/history/', PetHistoryViewAdmin.as_view(), name='api_pet_history_admin'),
    path('pet/<uuid:pk>/history/<int:hid>/', PetHistoryViewAdmin.as_view(), name='api_pet_history_admin'),

    #Appointment Management
    path('appointments/', AppointmentViewAdmin.as_view(), name='api_appointments_admin'),
    path('appointment/<int:pk>/', AppointmentViewAdmin.as_view(), name='api_appointment_detail_admin'),

]