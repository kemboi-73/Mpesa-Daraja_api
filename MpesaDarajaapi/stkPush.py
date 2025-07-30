from django.shortcuts import render
import requests
import json
import base64
from datetime import datetime
from django.http import JsonResponse
from .acesstokener import find_acesstoken
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Transaction
import os

@csrf_exempt
def start(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone = data.get('phone')
        amount = data.get('amount', 1)

        access_token_response = find_acesstoken(request)
        if isinstance(access_token_response, JsonResponse):
            access_token = access_token_response.content.decode('utf-8')
            access_token_json = json.loads(access_token)
            access_token = access_token_json.get('access_token')

            if access_token:
                process_request_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
                callback_url = os.environ.get("CALLBACK_URL")
                passkey = os.environ.get("PASSKEY")
                business_short_code = '174379'
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                password = base64.b64encode((business_short_code + passkey + timestamp).encode()).decode()

                stk_push_headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + access_token
                }

                stk_push_payload = {
                    'BusinessShortCode': business_short_code,
                    'Password': password,
                    'Timestamp': timestamp,
                    'TransactionType': 'CustomerPayBillOnline',
                    'Amount': amount,
                    'PartyA': phone,
                    'PartyB': business_short_code,
                    'PhoneNumber': phone,
                    'CallBackURL': callback_url,
                    'AccountReference': 'Mikes-MPESA DARAJA TEST',
                    'TransactionDesc': 'stkpush test'
                }

                try:
                    response = requests.post(process_request_url, headers=stk_push_headers, json=stk_push_payload)
                    response.raise_for_status()
                    response_data = response.json()

                    if response_data.get("ResponseCode") == "0":
                        Transaction.objects.create(
                            phone_number=phone,
                            amount=amount,
                            checkout_request_id=response_data.get("CheckoutRequestID"),
                            merchant_request_id=response_data.get("MerchantRequestID"),
                            status="Requested"
                        )
                        return JsonResponse({'CheckoutRequestID': response_data.get("CheckoutRequestID")})
                    else:
                        return JsonResponse({'error': 'Unknown response received.', 'details': response_data})

                except requests.exceptions.RequestException as e:
                    return JsonResponse({'error': str(e)})
            else:
                return JsonResponse({'error': 'Access token not found.'})
        else:
            return JsonResponse({'error': 'Failed to retrieve access token.'})

def stk_form_view(request):
    return render(request, 'stkform.html')
