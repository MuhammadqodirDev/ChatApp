from django.shortcuts import render, redirect
from django.views import View
# Create your views here.



class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            # Redirect to the login page
            return redirect('login')  # Adjust 'login' to your actual login URL name

        response = self.get_response(request)
        return response




class ChatView(View):
    def get(self, request):

        context = {
        }
        return render(request, 'index.html', context)



class LoginView(View):
    template_name = 'login.html'
    def get(self, request):

        context = {

        }
        return render(request, self.template_name, context)
    

class RegisterView(View):
    template_name = 'login.html'
    def get(self, request):

        context = {

        }
        return render(request, self.template_name, context)