from django.urls import path
from .views import auth_views, profile_views, saving_views, exchange_views, community_views, stocks_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,)
from rest_framework.authtoken.views import obtain_auth_token
from core.views.saving_views import fetch_and_store_savings_products

urlpatterns = [
    path('login/', auth_views.login_view, name='login'),
    path('signup/', auth_views.signup_view, name='signup'),
    path('profile/', profile_views.profile_view, name='profile'),
    path('api/fetch-savings-products/', fetch_and_store_savings_products, name='fetch_savings_products'),
    path('exchange/', exchange_views.exchange_rate, name='exchange'),
    path('community/', community_views.community_view, name='community'),
    path('stocks/', stocks_views.stock_summary, name='stocks'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
]
