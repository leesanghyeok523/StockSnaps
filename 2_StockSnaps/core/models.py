from django.db import models
from django.contrib.auth.models import AbstractUser

# 사용자 모델
class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    income_level = models.IntegerField(null=True, blank=True)
    member_number = models.CharField(max_length=50, null=True, blank=True)
    joined_products = models.JSONField(default=list, blank=True, null=True)  # JSON 필드로 상품 목록 저장

    def __str__(self):
        return self.username
    
# 금융기관 정보 모델 (fdrmEntyApi)
class FinancialInstitution(models.Model):
    institution_code = models.CharField(max_length=20, unique=True)
    institution_name = models.CharField(max_length=255)
    region = models.CharField(max_length=255, null=True, blank=True)  # 지역 정보
    phone_number = models.CharField(max_length=20, null=True, blank=True)  # 전화번호

class DepositProduct(models.Model):
    financial_company_code = models.CharField(max_length=20)
    financial_product_code = models.CharField(max_length=20)
    financial_product_name = models.CharField(max_length=255)
    join_way = models.CharField(max_length=100, null=True, blank=True)
    interest_rate_type = models.CharField(max_length=50, null=True, blank=True)
    interest_rate_type_name = models.CharField(max_length=50, null=True, blank=True)
    basic_interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    max_interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SavingsProduct(models.Model):
    financial_company_code = models.CharField(max_length=20)
    financial_product_code = models.CharField(max_length=20)
    financial_product_name = models.CharField(max_length=255)
    join_way = models.CharField(max_length=100, null=True, blank=True)
    interest_rate_type = models.CharField(max_length=50, null=True, blank=True)
    interest_rate_type_name = models.CharField(max_length=50, null=True, blank=True)
    basic_interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    max_interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    maturity_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Exchange(models.Model):
    cur_unit = models.CharField(max_length=10)  # 통화 코드 (예: USD, JPY 등)
    cur_nm = models.CharField(max_length=100)  # 통화 이름 (예: 미국 달러)
    ttb = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)  # 살 때 환율
    tts = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)  # 팔 때 환율
    deal_bas_r = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)  # 기준 환율
    bkpr = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)  # 장부가격
    yy_efee_r = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)  # 연 환가료율
    ten_dd_efee_r = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)  # 10일 환가료율
    kftc_deal_bas_r = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)  # 서울외국환중개 기준환율
    kftc_bkpr = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)  # 서울외국환중개 장부가격

    def __str__(self):
        return f"{self.cur_nm} ({self.cur_unit})"