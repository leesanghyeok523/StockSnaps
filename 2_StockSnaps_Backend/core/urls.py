from django.urls import path
from .views import (
    UserDetailView,
    DepositProductListView,
    DepositProductDetailView,
    UpdateJoinedProductsView,
    DeleteDepositProductView,
    JoinedProductsUpdateView, 
    SavingsProductListView,
    SavingsProductDetailView,
    FetchDepositProductsView,
    FetchSavingsProductsView,
)

urlpatterns = [
    path('user/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('update-joined-products/', UpdateJoinedProductsView.as_view(), name='update-joined-products'),
    path('delete-deposit-product/<int:product_id>/', DeleteDepositProductView.as_view(), name='delete-deposit-product'),
    path('joined-products/update/', JoinedProductsUpdateView.as_view(), name='update-joined-products'),
    path('fetch-deposit-products/', FetchDepositProductsView.as_view(), name='fetch-deposit-products'),
    path('fetch-savings-products/', FetchSavingsProductsView.as_view(), name='fetch-savings-products'),
    path('deposit-products/', DepositProductListView.as_view(), name='deposit-product-list'),
    path('savings-products/', SavingsProductListView.as_view(), name='savings-product-list'),
    path('deposits/', DepositProductListView.as_view(), name='deposit-list'),
    path('deposits/<int:pk>/', DepositProductDetailView.as_view(), name='deposit-detail'),
    path('savings/', SavingsProductListView.as_view(), name='savings-list'),
    path('savings/<int:pk>/', SavingsProductDetailView.as_view(), name='savings-detail'),
]
