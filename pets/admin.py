from django.contrib import admin
from . models import Pet, PetHistory, Appointment, PetCost

# Register your models here.

# admin.site.register(patient)
# admin.site.register(patient_history)
admin.site.register(Appointment)
admin.site.register(PetCost)

class PetCost(admin.TabularInline):
    model=PetCost

class PetAppointment(admin.TabularInline):
    model=Appointment

class PetHistoryAdmin(admin.ModelAdmin):
    list_display=('pet', 'assigned_doctor','admit_date','release_date')
    inlines=[PetAppointment, PetCost]

admin.site.register(PetHistory, PetHistoryAdmin)

class PetHistoryInline(admin.StackedInline):
    model=PetHistory
    
    
class PetAdmin(admin.ModelAdmin):
    list_display=('pet_name', 'pet_age','owner_address','owner_mobile', 'user',)
    inlines=[PetHistoryInline]

admin.site.register(Pet, PetAdmin)