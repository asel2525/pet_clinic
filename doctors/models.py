from django.db import models
from django.db.models.fields import DateField
from accounts.models import User




# Create your models here.

class Doctor(models.Model):

    address= models.TextField()
    mobile=models.CharField(max_length=20)
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    @property
    def get_name(self):
        return self.user.first_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{}".format(self.user.first_name)


