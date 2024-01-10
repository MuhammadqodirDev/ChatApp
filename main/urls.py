from django.urls import path
from main.views import *

urlpatterns = [
    path('', chat_view, name='chat_view')
]