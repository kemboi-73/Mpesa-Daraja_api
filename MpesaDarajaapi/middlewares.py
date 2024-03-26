from django.middleware.clickjacking import XFrameOptionsMiddleware

class CustomClickjackingMiddleware(XFrameOptionsMiddleware):
    def process_response(self, request, response):
        response = super().process_response(request, response)
        # Customize the response if needed
        return response
