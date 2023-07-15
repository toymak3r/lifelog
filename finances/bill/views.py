from django.shortcuts import render
<<<<<<< HEAD
from django.http import HttpResponse
from django.template import loader
from django.db.models import Sum
from .models import Bill

def index(request):
    bills = Bill.objects.all()
    total = Bill.objects.aggregate(total=Sum('value'))['total']
    template = loader.get_template('bills/index.html')
    context = {
        "bills": bills,
        "total": total
    }
    return HttpResponse(template.render(context, request))
=======

# Create your views here.
>>>>>>> 0e52eef (Initial django module for finances)
