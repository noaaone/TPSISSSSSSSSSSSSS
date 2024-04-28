from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        # Если пользователь существует и пароль верный, создаем новый токен
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
    else:
        return JsonResponse({'error': 'Неправильные учетные данные'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    # Удаляем текущий токен пользователя
    refresh_token = request.data.get('refresh')
    token = RefreshToken(refresh_token)
    token.blacklist()
    return JsonResponse({'message': 'Пользователь успешно разлогинен'})


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password or not email:
        return JsonResponse({'error': 'Пожалуйста, укажите имя пользователя, пароль и адрес электронной почты'},
                            status=400)

    # Проверяем, существует ли пользователь с таким именем
    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Пользователь с таким именем уже существует'}, status=400)

    # Создаем нового пользователя
    user = User.objects.create_user(username=username, password=password, email=email)

    return JsonResponse({'message': 'Пользователь успешно зарегистрирован'})