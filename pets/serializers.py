from django.db.models import fields
from django.db.models.query import QuerySet
from rest_framework import serializers
from accounts.models import User
from pets.models import Pet, PetHistory, Appointment
from django.contrib.auth.models import Group
from doctors.models import Doctor


class PetOwnerRegistrationSerializer(serializers.Serializer):
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

    def validate(self, data):
        password=data.get('password')
        password2=data.pop('password2')
        if password != password2:
            raise serializers.ValidationError({'password':'password must match'})
        return data
        
    def validate_password(self, password):
        if password.isdigit():
            raise serializers.ValidationError('Your password should contain letters!')
        return password  


    def create(self, validated_data):
        user = User.objects.create(
                username=validated_data['username'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                status=False
            )
        user.set_password(validated_data['password'])
        user.save()
        group_pet, created = Group.objects.get_or_create(name='pet')
        group_pet.user_set.add(user)
        return user
 

class PetProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['pet_name', 'pet_age', 'owner_address', 'owner_mobile',]

    def validate_mobile(self, owner_mobile):
        if owner_mobile.isdigit()==False:
            raise serializers.ValidationError('Please Enter a valid mobile number!')
        return owner_mobile
    
    def create(self, validated_data):
        new_pet= Pet.objects.create(
            pet_name=validated_data['pet_name'],
            pet_age=validated_data['pet_age'],
            owner_address=validated_data['owner_address'],
            owner_mobile=validated_data['owner_mobile'],
            user=validated_data['user']
        )
        return new_pet

    def update(self, instance, validated_data):
        instance.pet_name=validated_data.get('pet_name', instance.pet_name)
        instance.pet_age=validated_data.get('pet_age', instance.pet_age)
        instance.owner_address=validated_data.get('owner_address', instance.owner_address)
        instance.owner_mobile=validated_data.get('owner_mobile', instance.owner_mobile)
        instance.save()
        return instance



class PetCostSerializer(serializers.Serializer):
    room_charge=serializers.IntegerField(label="Оплата за комнату:")
    medicine_cost=serializers.IntegerField(label="Лекарства:")
    doctor_fee=serializers.IntegerField(label="Услуги доктора:")
    total_cost=serializers.CharField(label="Общая сумма:")


class AppointmentSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    appointment_date = serializers.DateField(label='Дата записи')
    appointment_time = serializers.TimeField(label='Время записи')
    status = serializers.BooleanField(required=False, read_only=True)
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), required=False)


    def create(self, validated_data):
        new_appointment= Appointment.objects.create(
            appointment_date=validated_data['appointment_date'],
            appointment_time=validated_data['appointment_time'],
            status=False,
            pet_history=validated_data['pet_history'],
            doctor=validated_data['doctor']
        )
        return new_appointment


class PetHistorySerializer(serializers.ModelSerializer):
    admit_date=serializers.DateField(label="Дата прибытия:", read_only=True)
    symptomps=serializers.CharField(label="Симптомы:", style={'base_template': 'textarea.html'})
    release_date=serializers.DateField(label="Дата выхода:", required=False)
    assigned_doctor=serializers.StringRelatedField(label='Назначенный доктор:')
    pet_appointments=AppointmentSerializer(label="Записи:",many=True)
    costs=PetCostSerializer()

