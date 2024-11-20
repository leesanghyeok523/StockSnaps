from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import DepositProduct, SavingsProduct, User
from .serializers import DepositProductSerializer, SavingsProductSerializer, UserSerializer
from django.conf import settings
import requests
from decimal import Decimal, InvalidOperation


# 단일 객체 조회
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

# 리스트 조회
class DepositProductListView(APIView):
    def get(self, request):
        products = DepositProduct.objects.all()
        serializer = DepositProductSerializer(products, many=True)
        return Response(serializer.data)

class SavingsProductListView(APIView):
    def get(self, request):
        products = SavingsProduct.objects.all()
        serializer = SavingsProductSerializer(products, many=True)
        return Response(serializer.data)

# POST 요청 처리
class UpdateJoinedProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        joined_products = request.data.get('joined_products', [])
        if isinstance(joined_products, list):
            user.joined_products = joined_products
            user.save()
            return Response({"message": "가입한 상품 목록이 업데이트되었습니다."}, status=status.HTTP_200_OK)
        return Response({"error": "유효한 데이터 형식이 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)

# DELETE 요청 처리
class DeleteDepositProductView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        product = get_object_or_404(DepositProduct, id=product_id)
        product.delete()
        return Response({"message": "상품이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)


class JoinedProductsUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        product_to_add = request.data.get('add', None)
        product_to_remove = request.data.get('remove', None)

        # 현재 joined_products를 리스트로 변환
        current_products = user.joined_products.split(',') if user.joined_products else []

        if product_to_add:
            current_products.append(product_to_add)
        if product_to_remove and product_to_remove in current_products:
            current_products.remove(product_to_remove)

        user.joined_products = ','.join(current_products)  # 쉼표로 구분하여 저장
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# 예금 상품 조회

class DepositProductListView(ListAPIView):
    queryset = DepositProduct.objects.all()
    serializer_class = DepositProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['financial_product_name', 'financial_company_code']

    def get_queryset(self):
        queryset = super().get_queryset()
        bank_name = self.request.query_params.get('bank_name')
        term = self.request.query_params.get('term')

        if bank_name:
            queryset = queryset.filter(financial_company_code=bank_name)
        if term:
            queryset = queryset.filter(join_way__icontains=term)  # 가입 방식 필터링

        return queryset

class DepositProductDetailView(RetrieveAPIView):
    queryset = DepositProduct.objects.all()
    serializer_class = DepositProductSerializer

# 적금 상품 조회

class SavingsProductListView(ListAPIView):
    queryset = SavingsProduct.objects.all()
    serializer_class = SavingsProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['financial_product_name', 'financial_company_code']

    def get_queryset(self):
        queryset = super().get_queryset()
        bank_name = self.request.query_params.get('bank_name')
        term = self.request.query_params.get('term')

        if bank_name:
            queryset = queryset.filter(financial_company_code=bank_name)
        if term:
            queryset = queryset.filter(join_way__icontains=term)

        return queryset

class SavingsProductDetailView(RetrieveAPIView):
    queryset = SavingsProduct.objects.all()
    serializer_class = SavingsProductSerializer

class DepositProductViewSet(ModelViewSet):
    queryset = DepositProduct.objects.all()
    serializer_class = DepositProductSerializer

class SavingsProductViewSet(ModelViewSet):
    queryset = SavingsProduct.objects.all()
    serializer_class = SavingsProductSerializer

class FetchDepositProductsView(APIView):
    permission_classes = [IsAdminUser]  # 관리자만 실행 가능

    def get(self, request):
        url = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"
        api_key = settings.FSS_API_KEY

        if not api_key:
            return Response({"error": "FSS_API_KEY is not set in the environment variables."}, status=500)

        params = {"auth": api_key, "topFinGrpNo": "020000", "pageNo": 1}
        current_page = 1
        created_products = []
        skipped_products = []

        while True:
            params["pageNo"] = current_page
            response = requests.get(url, params=params, timeout=10)

            if response.status_code != 200:
                return Response(
                    {"error": f"Failed to fetch data. Status code: {response.status_code}", "response": response.text},
                    status=response.status_code,
                )

            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError:
                return Response({"error": "Invalid JSON response from the API.", "response": response.text[:500]}, status=500)

            products = data.get("result", {}).get("baseList", [])
            if not products:
                break

            for product in products:
                obj, created = DepositProduct.objects.get_or_create(
                    financial_company_code=product.get("fin_co_no", "Unknown"),
                    financial_product_code=product.get("fin_prdt_cd", "Unknown"),
                    defaults={
                        "financial_product_name": product.get("fin_prdt_nm", "Unknown"),
                        "join_way": product.get("join_way", "N/A"),
                        "interest_rate_type": product.get("intr_rate_type", "N/A"),
                        "interest_rate_type_name": product.get("intr_rate_type_nm", "N/A"),
                        "basic_interest_rate": product.get("intr_rate", 0.0),
                        "max_interest_rate": product.get("intr_rate2", 0.0),
                    },
                )
                if created:
                    created_products.append(obj.financial_product_name)
                else:
                    skipped_products.append(obj.financial_product_name)

            current_page += 1
            max_page = data.get("result", {}).get("max_page_no", current_page)
            if current_page > max_page:
                break

        return Response(
            {
                "message": "Fetch operation completed.",
                "created_products": created_products,
                "skipped_products": skipped_products,
            }
        )
    
class FetchSavingsProductsView(APIView):
    permission_classes = [IsAdminUser]  # 관리자만 접근 가능

    def get(self, request):
        url = "http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"
        api_key = settings.FSS_API_KEY

        if not api_key:
            return Response({"error": "FSS_API_KEY is not set in the environment variables."}, status=500)

        params = {"auth": api_key, "topFinGrpNo": "020000", "pageNo": 1}
        current_page = 1
        created_products = []
        skipped_products = []

        while True:
            params["pageNo"] = current_page
            response = requests.get(url, params=params, timeout=10)

            if response.status_code != 200:
                return Response(
                    {"error": f"Failed to fetch data. Status code: {response.status_code}", "response": response.text},
                    status=response.status_code,
                )

            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError:
                return Response({"error": "Invalid JSON response from the API.", "response": response.text[:500]}, status=500)

            products = data.get("result", {}).get("baseList", [])
            if not products:
                break

            for product in products:
                try:
                    obj, created = SavingsProduct.objects.get_or_create(
                        financial_company_code=product.get("fin_co_no", "Unknown"),
                        financial_product_code=product.get("fin_prdt_cd", "Unknown"),
                        defaults={
                            "financial_product_name": product.get("fin_prdt_nm", "Unknown"),
                            "join_way": product.get("join_way", "N/A"),
                            "interest_rate_type": product.get("intr_rate_type", "N/A"),
                            "interest_rate_type_name": product.get("intr_rate_type_nm", "N/A"),
                            "basic_interest_rate": self.get_decimal_value(product.get("intr_rate", 0.0)),
                            "max_interest_rate": self.get_decimal_value(product.get("intr_rate2", 0.0)),
                            "maturity_amount": self.get_decimal_value(product.get("mtrt_int", None)),
                        },
                    )
                    if created:
                        created_products.append(obj.financial_product_name)
                    else:
                        skipped_products.append(obj.financial_product_name)
                except Exception as e:
                    return Response({"error": f"Error saving product: {str(e)}"}, status=500)

            current_page += 1
            max_page = data.get("result", {}).get("max_page_no", current_page)
            if current_page > max_page:
                break

        return Response(
            {
                "message": "Fetch operation completed.",
                "created_products": created_products,
                "skipped_products": skipped_products,
            }
        )

    def get_decimal_value(self, value):
        """
        Convert a value to Decimal if possible, otherwise return None.
        """
        if value is None or value == "":
            return None
        try:
            return Decimal(value)
        except (InvalidOperation, ValueError):
            return None