from django.db import models

class IncomeFrequency(models.Model):
    description = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)

    def __str__(self):
     return self.description


class Income(models.Model):
    description = models.CharField(max_length=300)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    frequence = models.ForeignKey(IncomeFrequency, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)

    def __str__(self):
     return self.description
