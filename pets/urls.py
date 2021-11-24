from .views import (RegistrationView, 
                    CustomAuthToken,
                    PetProfileView, 
                    PetHistoryView,
                    AppointmentView)

from django.urls import path


app_name='pets'
urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='api_pet_registration'),
    path('login/', CustomAuthToken.as_view(), name='api_pet_login'),
    path('profile/', PetProfileView.as_view(), name='api_pet_profile'),
    path('history/', PetHistoryView.as_view(), name='api_pet_history'),
    path('appointment/', AppointmentView.as_view(), name='api_pet_appointment'),

]
