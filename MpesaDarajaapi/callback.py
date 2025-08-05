import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from MpesaDarajaapi.models import Payment
from datetime import datetime

@csrf_exempt
def process_stk_callback(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method")

    try:
        stk_callback_response = json.loads(request.body)

        try:
            with open("Mpesastkresponse.json", "a") as log:
                json.dump(stk_callback_response, log)
                log.write("\n")
        except Exception as e:
            print("Failed to log callback:", e)

        stk_callback = stk_callback_response.get("Body", {}).get("stkCallback", {})
        print("Received Callback:", json.dumps(stk_callback, indent=2))

        merchant_request_id = stk_callback.get("MerchantRequestID")
        checkout_request_id = stk_callback.get("CheckoutRequestID")
        result_code = stk_callback.get("ResultCode")
        result_desc = stk_callback.get("ResultDesc")

        # Default None values
        amount = None
        transaction_id = None
        user_phone_number = None
        transaction_date = None

        # Extract metadata if present
        metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])
        for item in metadata:
            name = item.get("Name")
            value = item.get("Value")
            if name == "Amount":
                amount = value
            elif name == "MpesaReceiptNumber":
                transaction_id = value
            elif name == "PhoneNumber":
                user_phone_number = value
            elif name == "TransactionDate":
                try:
                    transaction_date = datetime.strptime(str(value), "%Y%m%d%H%M%S")
                except Exception:
                    transaction_date = None

        # Save or update payment
        Payment.objects.update_or_create(
            checkout_request_id=checkout_request_id,
            defaults={
                "merchant_request_id": merchant_request_id,
                "result_code": result_code,
                "result_desc": result_desc,
                "amount": amount,
                "transaction_id": transaction_id,
                "user_phone_number": user_phone_number,
                "transaction_date": transaction_date
            }
        )

        return JsonResponse({
            "message": "Payment record saved",
            "result_code": result_code,
            "result_desc": result_desc,
            "transaction_id": transaction_id,
            "amount": amount,
            "phone": user_phone_number,
            "transaction_date": transaction_date.strftime("%Y-%m-%d %H:%M:%S") if transaction_date else None
        })

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON format")
    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)
