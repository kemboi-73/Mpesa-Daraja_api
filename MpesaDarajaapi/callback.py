import json
from django.http import JsonResponse
from MpesaDarajaapi.models import Payment  # Make sure this import is correct

def process_stk_callback(request):
    stk_callback_response = json.loads(request.body)

    # Save response to a log file (optional)
    log_file = "Mpesastkresponse.json"
    with open(log_file, "a") as log:
        json.dump(stk_callback_response, log)

    # Extract necessary data
    merchant_request_id = stk_callback_response['Body']['stkCallback']['MerchantRequestID']
    checkout_request_id = stk_callback_response['Body']['stkCallback']['CheckoutRequestID']
    result_code = stk_callback_response['Body']['stkCallback']['ResultCode']
    result_desc = stk_callback_response['Body']['stkCallback']['ResultDesc']

    # Some callbacks may not contain CallbackMetadata if failed
    if result_code == 0:
        items = stk_callback_response['Body']['stkCallback']['CallbackMetadata']['Item']
        amount = items[0]['Value']
        transaction_id = items[1]['Value']
        user_phone_number = items[4]['Value']

        # ✅ Save to database
        Payment.objects.create(
            merchant_request_id=merchant_request_id,
            checkout_request_id=checkout_request_id,
            result_code=result_code,
            result_desc=result_desc,
            amount=amount,
            transaction_id=transaction_id,
            user_phone_number=user_phone_number
        )

        return JsonResponse({'message': 'Payment saved successfully'})
    else:
        # You can still save the failed attempt if needed
        Payment.objects.create(
            merchant_request_id=merchant_request_id,
            checkout_request_id=checkout_request_id,
            result_code=result_code,
            result_desc=result_desc,
        )
        return JsonResponse({'error': 'Payment failed'})
