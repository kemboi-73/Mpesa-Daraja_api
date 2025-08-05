import json
from datetime import datetime
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from MpesaDarajaapi.models import Payment

@csrf_exempt
def process_stk_callback(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method")

    try:
        stk_callback_response = json.loads(request.body)

        # Optional: Log callback to file for debugging
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

        amount = None
        transaction_id = None
        user_phone_number = None
        transaction_date = None

        if result_code == 0 and "CallbackMetadata" in stk_callback:
            metadata = stk_callback["CallbackMetadata"].get("Item", [])

            def get_metadata_value(name):
                for item in metadata:
                    if item.get("Name") == name:
                        return item.get("Value")
                return None

            amount = get_metadata_value("Amount")
            transaction_id = get_metadata_value("MpesaReceiptNumber")
            user_phone_number = get_metadata_value("PhoneNumber")

            # Parse date correctly
            transaction_date_str = get_metadata_value("TransactionDate")
            if transaction_date_str:
                try:
                    transaction_date = datetime.strptime(str(transaction_date_str), "%Y%m%d%H%M%S")
                except ValueError:
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
            "message": "Payment saved successfully" if result_code == 0 else "Payment failed",
            "transaction_id": transaction_id,
            "amount": amount,
            "phone": user_phone_number,
            "transaction_date": transaction_date.strftime("%Y-%m-%d %H:%M:%S") if transaction_date else None,
            "result_desc": result_desc
        })

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON format")
    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)
