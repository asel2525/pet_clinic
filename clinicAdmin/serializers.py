from rest_framework.exceptions import ValidationError
from pets.models import (Appointment,
                         PetHistory)
from rest_framework import serializers
from accounts.models import User
from doctors.models import Doctor
from django.contrib.auth.models import Group
from pets.models import Pet

class DoctorRegistrationSerializerAdmin(serializers.Serializer):

    username=serializers.CharField(label='Username:')
    first_name=serializers.CharField(label='First name:')
    last_name=serializers.CharField(label='Last name:', required=False)
    password = serializers.CharField(label='Password:',style={'input_type': 'password'}, write_only=True,min_length=8,
    help_text="Your password must contain at least 8 characters and should not be entirely numeric."
    )
    password2=serializers.CharField(label='Confirm password:',style={'input_type': 'password'},  write_only=True)
    
    

    
    def validate_username(self, username):
        username_exists=User.objects.filter(username__iexact=username)
        if username_exists:
            raise serializers.ValidationError({'username':'This username already exists'})
        return username

        
    def validate_password(self, password):
        if password.isdigit():
            raise serializers.ValidationError('Your password should contain letters!')
        return password  

 

    def validate(self, data):
        password=data.get('password')
        password2=data.pop('password2')
        if password != password2:
            raise serializers.ValidationError({'password':'password must match'})
        return data


    def create(self, validated_data):
        user= User.objects.create(
                username=validated_data['username'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                status=True,
            )
        user.set_password(validated_data['password'])
        user.save()
        group_doctor, created = Group.objects.get_or_create(name='doctor')
        group_doctor.user_set.add(user)
        return user


class DoctorRegistrationProfileSerializerAdmin(serializers.Serializer):

    address= serializers.CharField(label="Address:")
    mobile=serializers.CharField(label="Mobile Number:", max_length=20)


    def validate_mobile(self, mobile):
        if mobile.isdigit()==False:
            raise serializers.ValidationError('Please Enter a valid mobile number!')
        return mobile
    
    def create(self, validated_data):
        new_doctor= Doctor.objects.create(
            address=validated_data['address'],
            mobile=validated_data['mobile'],
            user=validated_data['user']
        )
        return new_doctor

class DoctorProfileSerializerAdmin(serializers.Serializer):
   
    address= serializers.CharField(label="Address:")
    mobile=serializers.CharField(label="Mobile Number:", max_length=20)


    def validate_mobile(self, mobile):
        if mobile.isdigit()==False:
            raise serializers.ValidationError('Please Enter a valid mobile number!')
        return mobile



class DoctorAccountSerializerAdmin(serializers.Serializer):
    id=serializers.UUIDField(read_only=True)
    username=serializers.CharField(label='Username:', read_only=True)
    first_name=serializers.CharField(label='First name:')
    last_name=serializers.CharField(label='Last name:', required=False)
    status=serializers.BooleanField(label='status')
    doctor=DoctorProfileSerializerAdmin(label='User')


    def update(self, instance, validated_data):
        try:
            doctor_profile=validated_data.pop('doctor')
        except:
            raise serializers.ValidationError("Please enter data related to doctor's profile")

        profile_data=instance.doctor

        instance.first_name=validated_data.get('first_name', instance.first_name)
        instance.last_name=validated_data.get('last_name', instance.last_name)
        instance.status=validated_data.get('status', instance.status)
        instance.save()

        profile_data.address=doctor_profile.get('address', profile_data.address)
        profile_data.mobile=doctor_profile.get('mobile', profile_data.mobile)
        profile_data.save()

        return instance


class AppointmentSerializerAdmin(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    appointment_date = serializers.DateField(label='Appointment date')
    appointment_time = serializers.TimeField(label='Appointement time')
    status = serializers.BooleanField(required=False)
    pet_history = serializers.PrimaryKeyRelatedField(queryset=PetHistory.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())


    def create(self, validated_data):
        new_appointment= Appointment.objects.create(
            appointment_date=validated_data['appointment_date'],
            appointment_time=validated_data['appointment_time'],
            status=True,
            pet_history=validated_data['pet_history'],
            doctor=validated_data['doctor']
        )
        return new_appointment
    

    def update(self, instance, validated_data):
        instance.appointment_date=validated_data.get('appointment_date', instance.appointment_date)
        instance.appointment_time=validated_data.get('appointment_time', instance.appointment_time)
        instance.status=validated_data.get('status', instance.status)
        instance.pet_history=validated_data.get('pet_history', instance.pet_history)
        instance.doctor=validated_data.get('doctor', instance.doctor)
        instance.save()

        return instance


class PetOwnerRegistrationSerializerAdmin(serializers.Serializer):

    username=serializers.CharField(label='Username:')
    first_name=serializers.CharField(label='First name:')
    last_name=serializers.CharField(label='Last name:', required=False)
    password = serializers.CharField(label='Password:',style={'input_type': 'password'}, write_only=True,min_length=8,
    help_text="Your password must contain at least 8 characters and should not be entirely numeric."
    )
    password2=serializers.CharField(label='Confirm password:',style={'input_type': 'password'},  write_only=True)
    

    
    def validate_username(self, username):
        username_exists=User.objects.filter(username__iexact=username)
        if username_exists:
            raise serializers.ValidationError({'username':'This username already exists'})
        return username

        
    def validate_password(self, password):
        if password.isdigit():
            raise serializers.ValidationError('Your password should contain letters!')
        return password  

 

    def validate(self, data):
        password=data.get('password')
        password2=data.pop('password2')
        if password != password2:
            raise serializers.ValidationError({'password':'password must match'})
        return data


    def create(self, validated_data):
        user= User.objects.create(
                username=validated_data['username'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                status=True
            )
        user.set_password(validated_data['password'])
        user.save()
        group_pet, created = Group.objects.get_or_create(name='pet')
        group_pet.user_set.add(user)
        return user


class PetRegistrationProfileSerializerAdmin(serializers.Serializer):
    pet_name = serializers.CharField(label="Name:",max_length=128)
    pet_age=serializers.DecimalField(label="Age:", max_digits=4,decimal_places=1)
    owner_address= serializers.CharField(label="Address:")
    owner_mobile=serializers.CharField(label="Mobile Number:", max_length=20)


    def validate_mobile(self, mobile):
        if mobile.isdigit()==False:
            raise serializers.ValidationError('Please Enter a valid mobile number!')
        return mobile
    
    def create(self, validated_data):
        new_pet= Pet.objects.create(
            pet_name=validated_data['pet_name'],
            pet_age=validated_data['pet_age'],
            owner_address=validated_data['owner_address'],
            owner_mobile=validated_data['owner_mobile'],
            user=validated_data['user']
        )
        return new_pet


class PetProfileSerializerAdmin(serializers.ModelSerializer):
    model = Pet
    fields = ['pet_name', 'pet_age', 'owner_address', 'owner_mobile', ]

    # pet_name = serializers.CharField(label="Name:", max_length=20)
    # pet_age=serializers.DecimalField(label="Age:", max_digits=4,decimal_places=1)
    # owner_address= serializers.CharField(label="Address:")
    # owner_mobile=serializers.CharField(label="Mobile Number:", max_length=20)

    def validate_mobile(self, mobile):
        if mobile.isdigit()==False:
            raise serializers.ValidationError('Please Enter a valid mobile number!')
        return mobile

class PetAccountSerializerAdmin(serializers.Serializer):
    id=serializers.UUIDField(read_only=True)
    username=serializers.CharField(label='Username:', read_only=True)
    first_name=serializers.CharField(label='First name:')
    last_name=serializers.CharField(label='Last name:', required=False)
    status=serializers.BooleanField(label='status')
    pet=PetProfileSerializerAdmin(label='User')


    def update(self, instance, validated_data):
        try:
            pet_profile=validated_data.pop('pet')
        except:
            raise serializers.ValidationError("Please enter data related to pet's profile")

        profile_data=instance.pet

        instance.first_name=validated_data.get('first_name', instance.first_name)
        instance.last_name=validated_data.get('last_name', instance.last_name)
        instance.status=validated_data.get('status', instance.status)
        instance.save()

        profile_data.pet_name=pet_profile.get('pet_name', profile_data.pet_name)
        profile_data.pet_age=pet_profile.get('pet_age', profile_data.pet_age)
        profile_data.owner_address=pet_profile.get('owner_address', profile_data.owner_address)
        profile_data.owner_mobile=pet_profile.get('owner_mobile', profile_data.owner_mobile)
        profile_data.save()

        return instance


class PetCostSerializer(serializers.Serializer):
    room_charge=serializers.IntegerField(label="Room Charge:")
    medicine_cost=serializers.IntegerField(label="Medicine Cost:")
    doctor_fee=serializers.IntegerField(label="Doctor Fee:")
    total_cost=serializers.CharField(label="Total Cost:")


class PetHistorySerializerAdmin(serializers.Serializer):

    id=serializers.IntegerField(read_only=True)
    admit_date=serializers.DateField(label="Admit Date:", read_only=True)
    symptomps=serializers.CharField(label="Symptomps:", style={'base_template': 'textarea.html'})
    release_date=serializers.DateField(label="Release Date:", required=False)
    assigned_doctor=serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())
    costs=PetCostSerializer(required=False)

    def update(self, instance, validated_data):
        try:
            updpated_cost=validated_data.pop('costs')
        except:
            raise serializers.ValidationError("Please enter data related to costs")

        saved_cost=instance.costs

        instance.admit_date=validated_data.get('admit_date', instance.admit_date)
        instance.symptomps=validated_data.get('symptomps', instance.symptomps)
        instance.release_date=validated_data.get('release_date', instance.release_date)
        instance.assigned_doctor=validated_data.get('assigned_doctor', instance.assigned_doctor)

        instance.save()

        saved_cost.room_charge= updpated_cost.get('room_charge', saved_cost.room_charge)
        saved_cost.medicine_cost= updpated_cost.get('medicine_cost', saved_cost.medicine_cost)
        saved_cost.doctor_fee= updpated_cost.get('doctor_fee', saved_cost.doctor_fee)

        saved_cost.save()

        return instance