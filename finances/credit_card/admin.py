from django.contrib import admin
from credit_card.models import CreditCard, CreditCardOperator

# Register your models here.
@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    
    def balance_to_pay(self, request):
        card = CreditCard.objects.get(id=request.id)
        limit = card.actual_limit
        limit_avaliable = card.limit_avaliable
        remaining_balance = limit - limit_avaliable
        return remaining_balance
    
    balance_to_pay.short_description = 'Remaining Balance To Pay'

    list_display = ('description', 'actual_limit', 'final_number', 'due_day', 'balance_to_pay')


@admin.register(CreditCardOperator)
class CreditCardOperatorAdmin(admin.ModelAdmin):
    pass

