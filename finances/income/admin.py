from django.contrib import admin
from income.models import Income, IncomeFrequency

# Register your models here.
@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    pass

@admin.register(IncomeFrequency)
class IncomeFrequencyAdmin(admin.ModelAdmin):
    pass
