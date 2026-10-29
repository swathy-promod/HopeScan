from django.db import models
from Guest.models import *

# Create your models here.
class tbl_slot(models.Model):
    slot_date=models.DateField()
    slot_fromtime=models.CharField(max_length=100)
    slot_totime=models.CharField(max_length=100)
    slot_count=models.CharField(max_length=100)
    doctor=models.ForeignKey(tbl_doctorregistration,on_delete=models.CASCADE)
    
