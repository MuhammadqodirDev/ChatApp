from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from main.models import *
from rest_framework.authtoken.models import Token



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            user = CustomUser.objects.filter(username=username).last()
            if not user or user.check_password(password) == False:
                raise Exception('Login yoki parol xato!!!')

            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'success': True,
                'token': token.key,
            })
        except Exception as e:
            return Response({
                'success': False,
                'meesage': f"Hatolik - {e}"
            }, status=400)


class Checkview(APIView):
    def get(self, request):
        return Response({})
    


# for i in CustomUser.objects.all():
#     Token.objects.get_or_create(user=i)