from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError

artfacts_fs = FileSystemStorage(location="files/artifacts/")


class BillPriority(models.Model):
    description = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)

    def __str__(self):
     return self.description

class BillType(models.Model):
    description = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)

    def __str__(self):
        return self.description

class BillFrequency(models.Model):
    description = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)

    def __str__(self) -> str:
       return self.description

class Bill(models.Model):
    type = models.ForeignKey(BillType, on_delete=models.DO_NOTHING)
    frequency = models.ForeignKey(BillFrequency, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=200)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    due_date = models.DateField(blank=True, null=True)
    due_day = models.IntegerField(validators=[MaxValueValidator(31)],)
    unique = models.BooleanField(default=True)
    artifact = models.FileField(storage=artfacts_fs, blank=True)
    quantity = models.IntegerField(default=1)
    obs = models.TextField(blank=True)
    priority = models.ForeignKey(BillPriority, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.description