from django.urls import path
from api.views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_view'),
    path('check/', Checkview.as_view(), name='check'),
]