from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .acesstokener import find_acesstoken
from .models import Payment
import requests
import json
import base64
import os
from datetime import datetime

@csrf_exempt
def run_query(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

    try:
        data = json.loads(request.body)
        checkout_request_id = data.get('CheckoutRequestID')

        if not checkout_request_id:
            return JsonResponse({'status': 'error', 'message': 'CheckoutRequestID is required.'}, status=400)

        # Try to get the payment from DB
        payment = Payment.objects.filter(checkout_request_id=checkout_request_id).first()
        if payment and payment.result_code == 0:
            # Already successful in DB — return instantly
            return JsonResponse({
                'status': 'success',
                'result_code': "0",
                'result_desc': payment.result_desc or "Payment successful",
                'user_message': "Payment was successful.",
                'transaction_details': {
                    "TransactionID": payment.transaction_id,
                    "Amount": str(payment.amount),
                    "PhoneNumber": payment.user_phone_number,
                    "TransactionDate": payment.transaction_date.strftime("%Y-%m-%d %H:%M:%S") if payment.transaction_date else "N/A"
                }
            })

        # Get access token for Safaricom query
        access_token_response = find_acesstoken(request)
        if not isinstance(access_token_response, JsonResponse):
            return JsonResponse({'status': 'error', 'message': 'Failed to retrieve access token.'}, status=500)

        access_token_data = json.loads(access_token_response.content.decode('utf-8'))
        access_token = access_token_data.get('access_token')

        if not access_token:
            return JsonResponse({'status': 'error', 'message': 'Access token missing from response.'}, status=500)

        # Prepare Safaricom query
        business_short_code = '174379'
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        passkey = os.environ.get("PASSKEY")
        if not passkey:
            return JsonResponse({'status': 'error', 'message': 'PASSKEY not set in environment variables.'}, status=500)

        password = base64.b64encode((business_short_code + passkey + timestamp).encode()).decode()

        query_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        payload = {
            'BusinessShortCode': business_short_code,
            'Password': password,
            'Timestamp': timestamp,
            'CheckoutRequestID': checkout_request_id
        }

        # Call Safaricom
        response = requests.post(query_url, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()

        result_code = str(response_data.get('ResultCode', ''))
        result_desc = response_data.get('ResultDesc', 'No description provided.')

        user_friendly_messages = {
            '0': "Payment was successful.",
            '1': "Insufficient balance in the M-PESA account.",
            '1032': "You cancelled the transaction.",
            '1037': "Timeout – You did not respond to the M-PESA prompt.",
            '2001': "Incorrect M-PESA PIN entered.",
            '1001': "Transaction is still in progress.",
            '9999': "An unknown error occurred.",
            '1025': "Failed to send the push request.",
            '1019': "Safaricom system did not respond in time."
        }
        user_message = user_friendly_messages.get(result_code, f"Unexpected Result Code: {result_code}")


        if payment:
            txn_details = {
                "TransactionID": payment.transaction_id or "N/A",
                "Amount": str(payment.amount) if payment.amount else "N/A",
                "PhoneNumber": payment.user_phone_number or "N/A",
                "TransactionDate": payment.transaction_date.strftime("%Y-%m-%d %H:%M:%S") if payment.transaction_date else "N/A"
            }
        else:
            txn_details = {
                "TransactionID": response_data.get("MpesaReceiptNumber", "N/A"),
                "Amount": response_data.get("Amount", "N/A"),
                "PhoneNumber": response_data.get("PhoneNumber", "N/A"),
                "TransactionDate": response_data.get("TransactionDate", "N/A")
            }

        # Return final JSON
        return JsonResponse({
            'status': 'success' if result_code == '0' else 'failed',
            'result_code': result_code,
            'result_desc': result_desc,
            'user_message': user_message,
            'transaction_details': txn_details
        })

    except requests.exceptions.RequestException as e:
        return JsonResponse({'status': 'error', 'message': f'Network error: {e}'}, status=500)

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON response received from Safaricom.'}, status=500)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Unexpected server error: {e}'}, status=500)
