import json
from django.http import JsonResponse


# Processses a callback url that is sent to the one who has a callback url 
def process_stk_callback(request):
    stk_callback_response = json.loads(request.body)

    # returns the response as a json format
    log_file = "Mpesastkresponse.json"
    with open(log_file, "a") as log:
        json.dump(stk_callback_response, log)

    #Names of the data in the order of how it will show up on a callback url
    
    merchant_request_id = stk_callback_response['Body']['stkCallback']['MerchantRequestID']

    checkout_request_id = stk_callback_response['Body']['stkCallback']['CheckoutRequestID']
    
    result_code = stk_callback_response['Body']['stkCallback']['ResultCode']
    result_desc = stk_callback_response['Body']['stkCallback']['ResultDesc']
    amount = stk_callback_response['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
    transaction_id = stk_callback_response['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
    user_phone_number = stk_callback_response['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value']

    # Error code handling based on the errors mentoned in query and stkPush file
    
    if result_code == 0:
        return JsonResponse({'message': 'Payment successful'})
    else:
        # Payment failed, handle accordingly
        
        # notify the user, retry the transaction, etc eg user canceled the stk request.
        return JsonResponse({'error': 'Payment failed'})
        
    # Code can be adedd to save the data into the database
