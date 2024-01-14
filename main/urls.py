from django.urls import path
from main.views import *

urlpatterns = [
    path('', ChatView.as_view(), name='chat_view'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
]