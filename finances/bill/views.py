import os
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db.models import Sum
from .models import Bill
from investments.coinbase.Coinbase import Coinbase
def calculate_percentage(value, total):
    if total == 0:
        return 0  # Avoid division by zero error
    percentage = (value / total) * 100
    return percentage


def index(request):
    bills = Bill.objects.all()
    total = Bill.objects.aggregate(total=Sum('value'))['total']

    coinbase = Coinbase(os.env['COINBASE_API_KEY'],
                        os.env['COINBASE_API_SECRET'])
    
    coinbase.update_balance()

    print(coinbase._coins)

    template = loader.get_template('bills/index.html')
    
    bills_pie_values = []
    for bill in bills:
        entry = {"name": bill.description, "y": float(calculate_percentage(bill.value, total)) }
        bills_pie_values.append(entry)

    coin_balance_gbp = sum(value['gbp'] for key, value in coinbase._coins.items() )

    context = {
        "coins": coinbase._coins,
        "coin_balance_gbp": coin_balance_gbp,
        "bills": bills,
        "total": total,
        "bills_pie_values": bills_pie_values
    }
    
    return HttpResponse(template.render(context, request))