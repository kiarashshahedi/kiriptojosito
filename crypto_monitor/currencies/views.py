# monitor/views.py
from django.shortcuts import render
from .models import CurrencyChange

def significant_changes(request):
    changes = CurrencyChange.objects.filter(price_change_percent__gt=1.0)
    return render(request, 'currencies/changes.html', {'changes': changes})
