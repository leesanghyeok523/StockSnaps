from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.models import CustomUser
from core.serializers import CustomUserSerializer


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'message': 'Login successful!'})
        return JsonResponse({'error': 'Invalid credentials'}, status=400)
    return render(request, 'login.html')  # 올바른 템플릿 경로

@api_view(['POST'])
def signup_view(request):
    """
    회원가입 API
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    subscribed_products = request.data.get('subscribed_products', '')

    if CustomUser.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    if CustomUser.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = CustomUser.objects.create_user(
        username=username,
        email=email,
        password=password,
        subscribed_products=','.join(subscribed_products) if subscribed_products else ''
    )

    serializer = CustomUserSerializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)