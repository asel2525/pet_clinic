from rest_framework.views import APIView
from .serializers import ( PetOwnerRegistrationSerializer,
                           PetProfileSerializer,
                           PetHistorySerializer,
                           AppointmentSerializer)

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from pets.models import Pet, PetHistory, Appointment
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission, AllowAny


class IsOwnerPet(BasePermission):
    """custom Permission class for Pet"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='pet').exists())


class CustomAuthToken(ObtainAuthToken):

    """This class returns custom Authentication token only for pet"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        account_approval = user.groups.filter(name='pet').exists()
        if user.status==False:
            return Response(
                {
                    'message': "Your account is not approved by admin yet!"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        elif account_approval==False:
            return Response(
                {
                    'message': "You are not authorised to login as a owner pet"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key
            },status=status.HTTP_200_OK)


class RegistrationView(APIView):
    """"API endpoint for Pet Registration"""

    permission_classes = []

    def post(self, request, format=None):
        registrationSerializer = PetOwnerRegistrationSerializer(
            data=request.data.get('user_data'))
        profileSerializer = PetProfileSerializer(
            data=request.data.get('profile_data'))
        checkregistration = registrationSerializer.is_valid()
        checkprofile = profileSerializer.is_valid()
        if checkregistration and checkprofile:
            pet = registrationSerializer.save()
            profileSerializer.save(user=pet)
            return Response({
                'user_data': registrationSerializer.data,
                'profile_data': profileSerializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'user_data': registrationSerializer.errors,
                'profile_data': profileSerializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class PetProfileView(APIView):
    """"API endpoint for Pet profile view/update-- Only accessble by owners"""
    permission_classes = [IsOwnerPet]


    def get(self, request, format=None):
        user = request.user
        profile = Pet.objects.filter(user=user).get()
        userSerializer=PetOwnerRegistrationSerializer(user)
        profileSerializer = PetProfileSerializer(profile)
        return Response({
            'user_data':userSerializer.data,
            'profile_data':profileSerializer.data

        }, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        user = request.user
        profile = Pet.objects.filter(user=user).get()
        profileSerializer = PetProfileSerializer(
            instance=profile, data=request.data.get('profile_data'), partial=True)
        if profileSerializer.is_valid():
            profileSerializer.save()
            return Response({
                'profile_data':profileSerializer.data
            }, status=status.HTTP_200_OK)
        return Response({
                'profile_data':profileSerializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class PetHistoryView(APIView):

    """"API endpoint for Pet history and costs view- Only accessble by owners"""
    permission_classes = [IsOwnerPet]

    def get(self, request, format=None):
        user = request.user
        user_pet = Pet.objects.filter(user=user).get()
        history = PetHistory.objects.filter(patient=user_pet)
        historySerializer=PetHistorySerializer(history, many=True)
        return Response(historySerializer.data, status=status.HTTP_200_OK)



class AppointmentView(APIView):
    """"API endpoint for getting appointments details, creating appointment"""
    permission_classes = [IsOwnerPet]
 

    def get(self, request,pk=None, format=None):
        user = request.user
        user_pet = Pet.objects.filter(user=user).get()
        history = PetHistory.objects.filter(patient=user_pet).latest('admit_date')
        appointment=Appointment.objects.filter(status=True,pet_history=history)
        historySerializer=AppointmentSerializer(appointment, many=True)
        return Response(historySerializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        user = request.user
        user_pet = Pet.objects.filter(user=user).get()
        history = PetHistory.objects.filter(pet=user_pet).latest('admit_date')
        serializer = AppointmentSerializer(
            data=request.data)
        if serializer.is_valid():
            serializer.save(pet_history=history)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response( serializer.errors
        , status=status.HTTP_400_BAD_REQUEST)



