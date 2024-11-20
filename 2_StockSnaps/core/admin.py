from django.contrib import admin
from core.models import User, FinancialInstitution, DepositProduct, SavingsProduct

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_of_birth', 'nickname', 'age', 'income_level')
    search_fields = ('username', 'email', 'nickname')

@admin.register(FinancialInstitution)
class FinancialInstitutionAdmin(admin.ModelAdmin):
    list_display = ('institution_code', 'institution_name', 'region', 'phone_number')
    search_fields = ('institution_code', 'institution_name')

@admin.register(DepositProduct)
class DepositProductAdmin(admin.ModelAdmin):
    list_display = ('financial_product_name', 'financial_company_code', 'basic_interest_rate', 'max_interest_rate')
    search_fields = ('financial_company_code', 'financial_product_name')

@admin.register(SavingsProduct)
class SavingsProductAdmin(admin.ModelAdmin):
    list_display = ('financial_product_name', 'financial_company_code', 'basic_interest_rate', 'max_interest_rate')
    search_fields = ('financial_company_code', 'financial_product_name')
