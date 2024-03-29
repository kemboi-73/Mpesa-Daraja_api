import requests
from django.http import JsonResponse

# generates an acesss token from safaricom servers

def find_acesstoken(request):
    consumer_key = "6LyDoxG9yJ9BTvRi0Cl9fKJRGoXFZNNx"  # app Consumer Key from safaricom
    consumer_secret = "NdXlNAEiFZWcYAjb"  # app Consumer Secret
    access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
    # Response
    
    headers = {'Content-Type': 'application/json'}
    auth = (consumer_key, consumer_secret)
    try:
        response = requests.get(access_token_url, headers=headers, auth=auth)
        # Raise exception for non-2xx status codes
        response.raise_for_status()  
        result = response.json()
        access_token = result['access_token']
        return JsonResponse({'access_token': access_token})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)})
    
