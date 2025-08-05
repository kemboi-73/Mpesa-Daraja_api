from django.shortcuts import render
from .main import main
from .acesstokener import find_acesstoken
from .stkPush import start
from .query import run_query
from .models import Transaction
from .models import Payment
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

def stk_form_view(request):
    return render(request, 'stkform.html')

from .models import Payment

def latest_payment(request):
    payment = Payment.objects.last()
    return render(request, 'payment_success.html', {'payment': payment})


def transaction_list(request):
    transactions = Payment.objects.all().order_by('-created_at')

    return render(request, 'transactions.html', {'transactions': transactions})


def get_latest_payment(request):
    latest = Payment.objects.last()
    if latest:
        return JsonResponse({
            'transaction_id': latest.transaction_id or "N/A",
            'amount': latest.amount or "N/A",
            'phone': latest.user_phone_number or "N/A",
            'result_desc': latest.result_desc or "N/A",
            'result_code': latest.result_code
        })
    else:
        return JsonResponse({'error': 'No payment found'}, status=404)
