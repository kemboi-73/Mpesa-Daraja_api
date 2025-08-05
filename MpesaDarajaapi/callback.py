import json
import logging
from datetime import datetime
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from MpesaDarajaapi.models import Payment

logger = logging.getLogger(__name__)

@csrf_exempt
def process_stk_callback(request):
    logger.info("STK Callback endpoint hit")

    if request.method != "POST":
        logger.warning("Invalid method used for callback")
        return HttpResponseBadRequest("Invalid request method")

    try:
        stk_callback_response = json.loads(request.body)

        # Optional logging to file for debugging
        try:
            with open("Mpesastkresponse.json", "a") as log:
                json.dump(stk_callback_response, log)
                log.write("\n")
        except Exception as e:
            logger.error(f"Failed to log callback: {e}")

        stk_callback = stk_callback_response.get("Body", {}).get("stkCallback", {})
        logger.info(f"Received Callback: {json.dumps(stk_callback, indent=2)}")

        merchant_request_id = stk_callback.get("MerchantRequestID")
        checkout_request_id = stk_callback.get("CheckoutRequestID")
        result_code = stk_callback.get("ResultCode")
        result_desc = stk_callback.get("ResultDesc")

        amount = None
        transaction_id = None
        user_phone_number = None
        transaction_date = None

        # If payment was successful, extract metadata
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

            # Convert TransactionDate to datetime
            raw_date = get_metadata_value("TransactionDate")
            if raw_date:
                try:
                    transaction_date = datetime.strptime(str(raw_date), "%Y%m%d%H%M%S")
                except ValueError:
                    logger.warning(f"⚠ Invalid transaction date format: {raw_date}")
                    transaction_date = None

        # Save payment to DB
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

        logger.info(f"Payment record updated for {checkout_request_id}")

        return JsonResponse({
            "message": "Payment saved successfully" if result_code == 0 else "Payment failed",
            "transaction_id": transaction_id,
            "amount": amount,
            "phone": user_phone_number,
            "transaction_date": transaction_date.strftime("%Y-%m-%d %H:%M:%S") if transaction_date else None,
            "result_desc": result_desc
        })

    except json.JSONDecodeError:
        logger.error("Invalid JSON format in callback")
        return HttpResponseBadRequest("Invalid JSON format")
    except Exception as e:
        logger.exception("Unexpected error processing callback")
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)
