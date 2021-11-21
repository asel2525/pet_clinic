from django.contrib import admin
from .models import Doctor
from pets.models import Appointment

# Register your models here.

class DoctorAppointment(admin.TabularInline):
    model=Appointment


# admin.site.register()

class doctorAdmin(admin.ModelAdmin):
    list_display=['get_name', 'address', 'mobile', 'user']
    inlines=[DoctorAppointment]


admin.site.register(Doctor,doctorAdmin)

