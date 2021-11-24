from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pets.models import (PetHistory,
                            Appointment)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group
from accounts.models import User
from . serializers import (DoctorAccountSerializerAdmin,
                           DoctorRegistrationSerializerAdmin,
                           DoctorRegistrationProfileSerializerAdmin,
                           AppointmentSerializerAdmin,
                           PetOwnerRegistrationSerializerAdmin,
                           PetRegistrationProfileSerializerAdmin,
                           PetAccountSerializerAdmin,
                           PetHistorySerializerAdmin)
from doctors.models import Doctor


class IsAdmin(BasePermission):
    """custom Permission class for Admin"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='admin').exists())


#Custom Auth token for Admin
class CustomAuthToken(ObtainAuthToken):

    """This class returns custom Authentication token only for admin"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        account_approval = user.groups.filter(name='admin').exists()
        if account_approval == False:
            return Response(
                {
                    'message': "You are not authorised to login as an admin"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        }, status=status.HTTP_200_OK)


class DocRegistrationViewAdmin(APIView):

    """API endpoint for creating doctor account- only accessible by Admin"""


    permission_classes = [IsAdmin]

    def post(self, request, format=None):
        registrationSerializer = DoctorRegistrationSerializerAdmin(
            data=request.data.get('user_data'))
        profileSerializer = DoctorRegistrationProfileSerializerAdmin(
            data=request.data.get('profile_data'))
        checkregistration = registrationSerializer.is_valid()
        checkprofile = profileSerializer.is_valid()
        if checkregistration and checkprofile:
            doctor = registrationSerializer.save()
            profileSerializer.save(user=doctor)
            return Response({
                'user_data': registrationSerializer.data,
                'profile_data': profileSerializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'user_data': registrationSerializer.errors,
                'profile_data': profileSerializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class DoctorAccountViewAdmin(APIView):

    """API endpoint for getiing info of all/particular doctor,
     update/delete doctor's info
     - only accessible by Admin"""

    permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):

        if pk:
            doctor_detail = self.get_object(pk)
            serializer = DoctorAccountSerializerAdmin(doctor_detail)
            return Response({'doctors': serializer.data}, status=status.HTTP_200_OK)
        all_doctor = User.objects.filter(groups=1, status=True)
        serializer = DoctorAccountSerializerAdmin(all_doctor, many=True)
        return Response({'doctors': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        saved_user = self.get_object(pk)
        serializer = DoctorAccountSerializerAdmin(
            instance=saved_user, data=request.data.get('doctors'), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'doctors': serializer.data}, status=status.HTTP_200_OK)
        return Response({
            'doctors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        saved_user = self.get_object(pk)
        saved_user.delete()
        return Response({"message": "User with id `{}` has been deleted.".format(pk)}, status=status.HTTP_204_NO_CONTENT)


class ApproveDoctorViewAdmin(APIView):
    """API endpoint for getting new doctor approval request, update and delete approval  request.
     - only accessible by Admin"""

    permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):

        if pk:
            doctor_detail = self.get_object(pk)
            serializer = DoctorAccountSerializerAdmin(doctor_detail)
            return Response({'doctors': serializer.data}, status=status.HTTP_200_OK)
        all_doctor = User.objects.filter(groups=1, status=False)
        serializer = DoctorAccountSerializerAdmin(all_doctor, many=True)
        return Response({'doctors': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        saved_user = self.get_object(pk)
        serializer = DoctorAccountSerializerAdmin(
            instance=saved_user, data=request.data.get('doctors'), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'doctors': serializer.data}, status=status.HTTP_200_OK)
        return Response({
            'doctors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        saved_user = self.get_object(pk)
        saved_user.delete()
        return Response({"message": "Doctor approval request with id `{}` has been deleted.".format(pk)}, status=status.HTTP_204_NO_CONTENT)


class ApprovePetViewAdmin(APIView):
    """API endpoint for getting new pet request,
     update and delete approval requests.- only accessible by Admin"""

    permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):

        if pk:
            doctor_detail = self.get_object(pk)
            serializer = PetAccountSerializerAdmin(doctor_detail)
            return Response({'pets': serializer.data}, status=status.HTTP_200_OK)
        all_pet = User.objects.filter(groups=2, status=False)
        serializer = PetAccountSerializerAdmin(all_pet, many=True)
        return Response({'pets': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        saved_user = self.get_object(pk)
        serializer = PetAccountSerializerAdmin(
            instance=saved_user, data=request.data.get('pets'), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'pets': serializer.data}, status=status.HTTP_200_OK)
        return Response({
            'pets': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        saved_user = self.get_object(pk)
        saved_user.delete()
        return Response({"message": "Pet approval request with id `{}` has been deleted.".format(pk)}, status=status.HTTP_204_NO_CONTENT)

class AppointmentViewAdmin(APIView):

    """API endpoint for getting info of all/particular appointment,
     update/delete appointment - only accessible by Admin"""

    permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):

        if pk:
            appointment_detail = self.get_object(pk)
            serializer = AppointmentSerializerAdmin(appointment_detail)
            return Response({'appointments': serializer.data}, status=status.HTTP_200_OK)
        all_appointment = Appointment.objects.filter(status=True)
        serializer = AppointmentSerializerAdmin(all_appointment, many=True)
        return Response({'appointments': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = AppointmentSerializerAdmin(
            data=request.data.get('appointments'))
        if serializer.is_valid():
            serializer.save()
            return Response({
                'appointments': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response({
            'appointments': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        saved_appointment= self.get_object(pk)
        serializer = AppointmentSerializerAdmin(
            instance=saved_appointment, data=request.data.get('appointments'), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'appointments': serializer.data}, status=status.HTTP_200_OK)
        return Response({
            'appointments': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)    

    def delete(self, request, pk):
        saved_appointment= self.get_object(pk)
        saved_appointment.delete()
        return Response({"message": "Appointment with id `{}` has been deleted.".format(pk)}, status=status.HTTP_204_NO_CONTENT)


class ApproveAppointmentViewAdmin(APIView):
    """API endpoint for getting info of all/particular unapproved appointment,
     update/delete  unapproved appointment - only accessible by Admin"""

    permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404
    
    def get(self, request, pk=None, format=None):

        if pk:
            appointment_detail = self.get_object(pk)
            serializer = AppointmentSerializerAdmin(appointment_detail)
            return Response({'appointments': serializer.data}, status=status.HTTP_200_OK)
        all_appointment = Appointment.objects.filter(status=False)
        serializer = AppointmentSerializerAdmin(all_appointment, many=True)
        return Response({'appointments': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
            saved_appointment= self.get_object(pk)
            serializer = AppointmentSerializerAdmin(
                instance=saved_appointment, data=request.data.get('appointments'), partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'appointments': serializer.data}, status=status.HTTP_200_OK)
            return Response({
                'appointments': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        saved_appointment= self.get_object(pk)
        saved_appointment.delete()
        return Response({"message": "Appointment with id `{}` has been deleted.".format(pk)}, status=status.HTTP_204_NO_CONTENT)


class PetRegistrationViewAdmin(APIView):
    """API endpoint for creating patients account- only accessible by Admin"""

    permission_classes = [IsAdmin]

    def post(self, request, format=None):
        registrationSerializer = PetOwnerRegistrationSerializerAdmin(
            data=request.data.get('user_data'))
        profileSerializer = PetRegistrationProfileSerializerAdmin(
            data=request.data.get('profile_data'))
        checkregistration = registrationSerializer.is_valid()
        checkprofile = profileSerializer.is_valid()
        if checkregistration and checkprofile:
            patient = registrationSerializer.save()
            profileSerializer.save(user=patient)
            return Response({
                'user_data': registrationSerializer.data,
                'profile_data': profileSerializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'user_data': registrationSerializer.errors,
                'profile_data': profileSerializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class PetAccountViewAdmin(APIView):

    """API endpoint for getiing info of all/particular pet,
     update/delete pet's info
     - only accessible by Admin"""

    permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):

        if pk:
            pet_detail = self.get_object(pk)
            serializer = PetAccountSerializerAdmin(pet_detail)
            return Response({'pets': serializer.data}, status=status.HTTP_200_OK)
        all_pet = User.objects.filter(groups=2, status=True)
        serializer = PetAccountSerializerAdmin(all_pet, many=True)
        return Response({'pets': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        saved_user = self.get_object(pk)
        serializer = PetAccountSerializerAdmin(
            instance=saved_user, data=request.data.get('pets'), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'pets': serializer.data}, status=status.HTTP_200_OK)
        return Response({
            'pets': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        saved_user = self.get_object(pk)
        saved_user.delete()
        return Response({"message": "User with id `{}` has been deleted.".format(pk)}, status=status.HTTP_204_NO_CONTENT)

class PetHistoryViewAdmin(APIView):
    """API endpoint for getting info of all/particular patient's history,
     update/delete patient's history info
     - only accessible by Admin"""

    permission_classes = [IsAdmin]
    
    
    def get(self, request, pk, hid=None, format=None):
        user_pet = get_object_or_404(User,pk=pk).pet
        if hid:
            try:
                history=PetHistory.objects.get(id=hid)
            except PetHistory.DoesNotExist:
                raise Http404
            if history.pet==user_pet:
                serializer = PetHistorySerializerAdmin(history)
                return Response({'pet_history': serializer.data}, status=status.HTTP_200_OK)
            return Response({"message: This history id `{}` does not belong to the user".format(hid)}, status=status.HTTP_404_NOT_FOUND)

        
        pet_historys=user_pet.patient_history_set.all()
        serializer = PetHistorySerializerAdmin(pet_historys, many=True)
        return Response({'pet_history': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk, hid):
        user_pet = get_object_or_404(User,pk=pk).pet
        try:
            history=PetHistory.objects.get(id=hid)
        except PetHistory.DoesNotExist:
            raise Http404
        if history.pet==user_pet:
            serializer = PetHistorySerializerAdmin(instance=history,data=request.data.get('pet_history'), partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'pet_history': serializer.data}, status=status.HTTP_200_OK)
            return Response({'pet_history': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message: This history id `{}` does not belong to the user".format(hid)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, hid):
        user_pet = get_object_or_404(User,pk=pk).pet
        try:
            history=PetHistory.objects.get(id=hid)
        except PetHistory.DoesNotExist:
            raise Http404
        if history.pet==user_pet:
            history.delete()
            return Response({"message": "History with id `{}` has been deleted.".format(hid)}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message: This history id `{}` does not belong to the user".format(hid)}, status=status.HTTP_404_NOT_FOUND)

