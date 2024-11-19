from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Profile  # 수정된 경로
from core.serializers import ProfileSerializer
from django.shortcuts import render, redirect

@api_view(['GET'])
def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('/login/')  # 로그인 페이지로 리다이렉트
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})
