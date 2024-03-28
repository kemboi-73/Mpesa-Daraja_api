import requests
from django.http import JsonResponse

def main (request):
    return JsonResponse({'error': 'main page'})  