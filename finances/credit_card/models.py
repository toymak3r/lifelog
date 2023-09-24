from django.db import models
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError


class CreditCardOperator(models.Model):
    description = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)

    def __str__(self):
        return self.description


class CreditCard(models.Model):
    type = models.ForeignKey(CreditCardOperator, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=200)
    actual_limit = models.DecimalField(max_digits=100, decimal_places=2)
    due_day = models.IntegerField(validators=[MaxValueValidator(31)],)
    obs = models.TextField(blank=True)
    final_number = models.TextField(blank=False)
    limit_avaliable = models.DecimalField(max_digits=100, decimal_places=2)
    interest = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return self.description
