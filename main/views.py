from django.shortcuts import render, redirect
from django.views import View
from main.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
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
    template_name = 'index.html'
    def get(self, request):
        room_id = request.GET.get('room')

        user = request.user
        chats = Chat.objects.filter(participants__in=[user])

        context = {
            'user_chats': chats
        }
        if room_id:
            chat = Chat.objects.get(id=room_id)
            messages = Message.objects.filter(chat=chat)
            context['chat_messages'] = messages
            context['selected_chat'] = chat
        return render(request, self.template_name, context)



class LoginView(View):
    template_name = 'login.html'
    def get(self, request):
        context = {

        }
        return render(request, self.template_name, context)

    def post(self, request):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            remember_me = request.POST.get('remember_me')

            user = CustomUser.objects.filter(username=username).last()
            if not user or user.check_password(password) == False:
                raise Exception('Username or Password is incorrect!!!')

            auth_login(request, user)

            if not remember_me:
                request.session.set_expiry(0)
            return redirect('chat_view')
        
        except Exception as e:
            messages.error(request, f'Error - {e}')
            return redirect('/')
    

class RegisterView(View):
    template_name = 'signup.html'
    def get(self, request):

        context = {

        }
        return render(request, self.template_name, context)
    def post(self, request):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            password1 = request.POST.get('password1')
            first_name = request.POST.get('first_name')
            
            if password == password1:
                if not CustomUser.objects.filter(username=username).exists():
                    user = CustomUser.objects.create(
                        username=username,
                        password=password,
                        first_name=first_name,
                    )
                    auth_login(request, user)
                else:
                    raise Exception('Username Already exists!')
            else:
                raise Exception('Passwords are not th same!')

            return redirect('/')
            # return render(request, self.template_name, context)
        except Exception as e:
            messages.error(request, f'Error - {e}')
            return redirect('register')
    

def logout(request):
    auth_logout(request)
    return redirect('login')