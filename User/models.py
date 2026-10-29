from django.db import models
from Guest.models import *
from Doctor.models import *

# Create your models here.
class tbl_complaint(models.Model):
    complaint_title=models.CharField(max_length=30)
    complaint_content=models.CharField(max_length=100)
    complaint_date=models.DateField(auto_now_add=True)
    complaint_status=models.IntegerField(default=0)
    complaint_reply=models.CharField(max_length=50)
    user=models.ForeignKey(tbl_userregistration,on_delete=models.CASCADE)
    
class tbl_feedback(models.Model):
    feedback_content=models.CharField(max_length=30)
    feedback_date=models.DateField(auto_now_add=True)
    user=models.ForeignKey(tbl_userregistration,on_delete=models.CASCADE,null=True,blank=True)



class tbl_booking(models.Model):
    booking_date=models.DateField(auto_now_add=True)
    booking_time=models.TimeField()
    booking_amount=models.CharField(max_length=100)
    booking_status=models.IntegerField(default=0)
    slot=models.ForeignKey(tbl_slot,on_delete=models.CASCADE)
    user=models.ForeignKey(tbl_userregistration,on_delete=models.CASCADE)

    