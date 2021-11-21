from django.db import models
from accounts.models import User
from doctors.models import Doctor


class Pet(models.Model):
    pet_name = models.CharField(max_length=128)
    pet_age = models.DecimalField(max_digits=4, decimal_places=1)
    owner_address = models.TextField(default=1)
    owner_mobile = models.CharField(max_length=128)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.username


class PetHistory(models.Model):
    admit_date=models.DateField(verbose_name="Дата прибытия",auto_now=False, auto_now_add=True)
    symptomps=models.TextField()
    release_date=models.DateField(verbose_name="Дата выхода",auto_now=False, auto_now_add=False, null=True, blank=True)
    pet=models.ForeignKey(Pet, on_delete=models.CASCADE)
    assigned_doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return self.pet.get_name


class Appointment(models.Model):
    appointment_date = models.DateField(verbose_name="Дата записи",auto_now=False, auto_now_add=False)
    appointment_time=models.TimeField(verbose_name="Время записи", auto_now=False, auto_now_add=False)
    status=models.BooleanField(default=False)
    pet_history=models.ForeignKey(PetHistory,related_name='patient_appointments', on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctor,related_name='doctor_appointments',null=True, on_delete=models.SET_NULL)

    @property
    def pet_name(self):
        self.pet_history.pet.get_name 

    def __str__(self):
        return self.pet_history.pet.get_name+' '+self.doctor.get_name

class PetCost(models.Model):
    room_charge=models.PositiveIntegerField(verbose_name="Оплата за комнату", null=False)
    medicine_cost=models.PositiveIntegerField(verbose_name="Лекарства", null=False)
    doctor_fee=models.PositiveIntegerField(verbose_name="Услуги доктора", null=False)
    pet_details=models.OneToOneField(PetHistory, related_name='costs', on_delete=models.CASCADE)

    @property
    def total_cost(self):
        return "{} tk" .format(self.room_charge+self.medicine_cost+self.doctor_fee)
    
    def __str__(self):
        return self.pet_details.pet.get_name+'-'+str(self.pet_details.admit_date)
    
