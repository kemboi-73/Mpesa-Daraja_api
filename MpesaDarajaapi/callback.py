import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from MpesaDarajaapi.models import Payment 

@csrf_exempt
def process_stk_callback(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method")

    try:
        stk_callback_response = json.loads(request.body)

        # Optional logging
        try:
            with open("Mpesastkresponse.json", "a") as log:
                json.dump(stk_callback_response, log)
                log.write("\n")
        except Exception as e:
            print("Failed to log callback:", e)

        stk_callback = stk_callback_response.get("Body", {}).get("stkCallback", {})

        merchant_request_id = stk_callback.get("MerchantRequestID")
        checkout_request_id = stk_callback.get("CheckoutRequestID")
        result_code = stk_callback.get("ResultCode")
        result_desc = stk_callback.get("ResultDesc")

        if result_code == 0 and "CallbackMetadata" in stk_callback:
            metadata = stk_callback["CallbackMetadata"].get("Item", [])

            # Extracts values safely from metadata
            def get_metadata_value(name):
                for item in metadata:
                    if item.get("Name") == name:
                        return item.get("Value")
                return None

            amount = get_metadata_value("Amount")
            transaction_id = get_metadata_value("MpesaReceiptNumber")
            user_phone_number = get_metadata_value("PhoneNumber")

            Payment.objects.create(
                merchant_request_id=merchant_request_id,
                checkout_request_id=checkout_request_id,
                result_code=result_code,
                result_desc=result_desc,
                amount=amount,
                transaction_id=transaction_id,
                user_phone_number=user_phone_number
            )
            return JsonResponse({"message": "Payment saved successfully"})

        # If payment failed
        Payment.objects.create(
            merchant_request_id=merchant_request_id,
            checkout_request_id=checkout_request_id,
            result_code=result_code,
            result_desc=result_desc
        )
        return JsonResponse({"error": "Payment failed"})

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON format")
    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)
