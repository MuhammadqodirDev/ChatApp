from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_paths = [reverse('login'), reverse('register')]

    def __call__(self, request):
        path = request.path_info
        if not request.user.is_authenticated and path not in self.exempt_paths:
            # Redirect to the login page
            return redirect('login')  # Adjust 'login' to your actual login URL name

        response = self.get_response(request)
        return response
