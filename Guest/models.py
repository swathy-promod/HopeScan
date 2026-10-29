from django.db import models
from Administrator .models import *
class tbl_userregistration(models.Model):
    userregistration_name=models.CharField(max_length=100)
    userregistration_email=models.CharField(max_length=100)
    userregistration_contact=models.CharField(max_length=100)
    userregistration_address=models.CharField(max_length=100)
    userregistration_gender=models.CharField(max_length=100)
    userregistration_dateofbirth=models.DateField(max_length=100)
    userregistration_place=models.ForeignKey(tbl_place,on_delete=models.CASCADE,null=True,blank=True)
    userregistration_photo=models.FileField(upload_to='Assets/User/Photos')
    userregistration_password=models.CharField(max_length=100)
    user_status = models.IntegerField(default=0)

class tbl_doctorregistration(models.Model):
    doctorregistration_name=models.CharField(max_length=100)
    doctorregistration_email=models.CharField(max_length=100)
    doctorregistration_contact=models.CharField(max_length=100)
    doctorregistration_address=models.CharField(max_length=100)
    doctorregistration_gender=models.CharField(max_length=100)
    doctorregistration_place=models.ForeignKey(tbl_place,on_delete=models.CASCADE,null=True,blank=True)
    doctorregistration_photo=models.FileField(upload_to='Assets/User/Photos')
    doctorregistration_proof=models.FileField(upload_to='Assets/User/Proof')
    doctorregistration_password=models.CharField(max_length=100)
    doctorregistration_exp=models.CharField(max_length=100)
    doctor_status = models.IntegerField(default=0)

# Create your models here.
           