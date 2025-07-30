import requests
from django.http import JsonResponse
from requests.auth import HTTPBasicAuth
from django.conf import settings

def find_acesstoken(request):
    consumer_key = settings.CONSUMER_KEY
    consumer_secret = settings.CONSUMER_SECRET
    access_token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    try:
        response = requests.get(
            access_token_url,
            auth=HTTPBasicAuth(consumer_key, consumer_secret),
            timeout=10  # prevent hanging if Safaricom API is down
        )
        response.raise_for_status()  # raises HTTPError for bad responses

        data = response.json()
        access_token = data.get('access_token')

        if not access_token:
            return JsonResponse({'error': 'Access token not found in response', 'raw': data}, status=500)

        return JsonResponse({'access_token': access_token})

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': 'Failed to get access token', 'details': str(e)}, status=500)
