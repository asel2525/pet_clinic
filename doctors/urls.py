from .views import RegistrationView, CustomAuthToken, DoctorProfileView, doctorAppointmentView
from django.urls import path


app_name='doctor'
urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='api_doctor_registration'),
    path('login/', CustomAuthToken.as_view(), name='api_doctor_login'),
    path('profile/', DoctorProfileView.as_view(), name='api_doctor_profile'),
    path('appointments/', doctorAppointmentView.as_view(), name='api_doctor_profile'),


]