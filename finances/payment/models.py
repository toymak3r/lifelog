from django.db import models
from django.core.files.storage import FileSystemStorage

from bill.models import Bill
from income.models import Income

receipt_artfacts_fs = FileSystemStorage(location="files/artifacts/")

class PaymentMethod(models.Model):
   description = models.CharField(max_length=200)
   slug = models.CharField(max_length=200)

   def __str__(self):
     return self.description


class Payment(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    receipt_artifact = models.ImageField(storage=receipt_artfacts_fs)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    method = models.ForeignKey(PaymentMethod, on_delete=models.DO_NOTHING)
    
    def __str__(self):
     return self.bill.description
    

class PaymentCards(models.Model):
   description = models.CharField(max_length=200)
   slug = models.CharField(max_length=200)
   limit = models.DecimalField(max_digits=6, decimal_places=2)

   def __str__(self):
     return self.description