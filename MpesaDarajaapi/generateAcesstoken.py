import requests
from django.http import JsonResponse

def get_access_token(request):
    consumer_key = "6LyDoxG9yJ9BTvRi0Cl9fKJRGoXFZNNx"  # Fill with your app Consumer Key
    consumer_secret = "NdXlNAEiFZWcYAjb"  # Fill with your app Consumer Secret
    access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    headers = {'Content-Type': 'application/json'}
    auth = (consumer_key, consumer_secret)
    try:
        response = requests.get(access_token_url, headers=headers, auth=auth)
        response.raise_for_status()  # Raise exception for non-2xx status codes
        result = response.json()
        access_token = result['access_token']
        return JsonResponse({'access_token': access_token})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)})
    