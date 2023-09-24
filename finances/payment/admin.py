from django.contrib import admin
from payment.models import Payment, PaymentMethod

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('bill', 'date', 'method')

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    pass