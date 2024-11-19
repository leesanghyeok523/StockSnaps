from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# 사용자 프로필
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 수정
    nickname = models.CharField(max_length=50)
    age = models.IntegerField()
    income_level = models.IntegerField(default=0)

# 예적금 상품 데이터
class SavingsProduct(models.Model):
    bank_name = models.CharField(max_length=255)  # 은행명
    product_name = models.CharField(max_length=255)  # 상품명
    interest_rate = models.FloatField()  # 기본 금리
    preferential_rate = models.FloatField(null=True, blank=True,default=0.0)  # 우대 금리
    term = models.IntegerField()  # 가입 기간 (개월)
    min_amount = models.DecimalField(max_digits=15, decimal_places=2)  # 최소 가입 금액
    max_amount = models.DecimalField(max_digits=15, decimal_places=2)  # 최대 가입 금액
    rate_type = models.CharField(max_length=50)  # 금리 유형 (고정/변동)
    join_conditions = models.TextField(null=True, blank=True)  # 가입 조건
    created_at = models.DateTimeField(auto_now_add=True)  # 데이터 생성 시간

    class Meta:
        unique_together = ['bank_name', 'product_name', 'term']  # 중복 방지 필드 설정

# 게시판 게시글
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 수정
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# 주식 데이터
class Stock(models.Model):
    stock_name = models.CharField(max_length=255)
    ticker_symbol = models.CharField(max_length=50)
    dividend_yield = models.FloatField()
    performance = models.JSONField()  # JSON 형식으로 저장

# 주식 요약 보고서
class StockReport(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=50)  # 분기 / 연간
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    subscribed_products = models.TextField(blank=True, null=True)

    def get_subscribed_products(self):
        """쉼표로 구분된 텍스트를 리스트로 변환"""
        if self.subscribed_products:
            return self.subscribed_products.split(',')
        return []