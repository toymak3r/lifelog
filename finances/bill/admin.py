from django.contrib import admin
from bill.models import Bill, BillFrequency, BillPriority, BillType, Currency

# Register your models here.

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass

class BillAdmin(admin.ModelAdmin):
    list_display = ('description', 'type', 'due_day',
                    'due_date', 'value', 'priority')


@admin.register(BillFrequency)
class BillFrequencyAdmin(admin.ModelAdmin):
    pass


@admin.register(BillPriority)
class BillPriorityAdmin(admin.ModelAdmin):
    pass


@admin.register(BillType)
class BillTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Bill, BillAdmin)
