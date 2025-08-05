from django.shortcuts import render
from .main import main
from .acesstokener import find_acesstoken
from .stkPush import start
from .query import run_query
from .models import Transaction
from .models import Payment

def stk_form_view(request):
    return render(request, 'stkform.html')

from .models import Payment

def latest_payment(request):
    payment = Payment.objects.last()
    return render(request, 'payment_success.html', {'payment': payment})


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Transaction

# @csrf_exempt
# def mpesa_callback(request):
#     data = json.loads(request.body)
#     stk_callback = data['Body']['stkCallback']
#     checkout_request_id = stk_callback['CheckoutRequestID']
#     result_code = stk_callback['ResultCode']
#     result_desc = stk_callback['ResultDesc']

#     transaction = Transaction.objects.filter(checkout_request_id=checkout_request_id).first()
#     if transaction:
#         transaction.status = "Success" if result_code == 0 else f"Failed: {result_desc}"
#         transaction.save()

#     return JsonResponse({"status": "ok"})


def transaction_list(request):
    transactions = Payment.objects.all().order_by('-created_at')

    return render(request, 'transactions.html', {'transactions': transactions})

from django.http import JsonResponse
from .models import Payment

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
