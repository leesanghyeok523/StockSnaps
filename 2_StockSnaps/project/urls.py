from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import DepositProductViewSet, SavingsProductViewSet

router = DefaultRouter()
router.register(r'deposits', DepositProductViewSet, basename='depositproduct')
router.register(r'savings', SavingsProductViewSet, basename='savingsproduct')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/core/router/', include(router.urls)),  # Router URL
    path('api/core/actions/', include('core.urls')),  # 비-Router URL
    path('api/auth/', include('dj_rest_auth.urls')),  # 로그인/로그아웃
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),  # 회원가입
]
