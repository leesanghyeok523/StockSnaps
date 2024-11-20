import requests
from django.core.management.base import BaseCommand
from core.models import SavingsProduct
from decouple import config
from decimal import Decimal, InvalidOperation


class Command(BaseCommand):
    help = "Fetch savings products from external API and save them to the database."

    def handle(self, *args, **kwargs):
        url = "http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"  # 적금 API URL
        api_key = config('FSS_API_KEY')  # 환경 변수에서 API 키 가져오기

        if not api_key:
            self.stderr.write("FSS_API_KEY is not set in the environment variables.")
            return

        params = {"auth": api_key, "topFinGrpNo": "020000", "pageNo": 1}
        current_page = 1

        while True:
            params["pageNo"] = current_page
            response = requests.get(url, params=params, timeout=10)

            if response.status_code != 200:
                self.stderr.write(f"Failed to fetch data. Status code: {response.status_code}")
                self.stderr.write(f"Response content: {response.text}")
                return

            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError:
                self.stderr.write("The API did not return valid JSON.")
                self.stderr.write(f"Response content: {response.text[:500]}")
                return

            products = data.get("result", {}).get("baseList", [])
            if not products:
                self.stdout.write(f"No products found on page {current_page}.")
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
                            # 숫자로 변환 가능한 값만 저장
                            "basic_interest_rate": self.get_decimal_value(product.get("intr_rate", 0.0)),
                            "max_interest_rate": self.get_decimal_value(product.get("intr_rate2", 0.0)),
                            "maturity_amount": self.get_decimal_value(product.get("mtrt_int", None)),
                        },
                    )
                    if created:
                        self.stdout.write(f"Created: {obj.financial_product_name}")
                    else:
                        self.stdout.write(f"Skipped: {obj.financial_product_name}")
                except Exception as e:
                    self.stderr.write(f"Error saving product {product.get('fin_prdt_nm', 'Unknown')}: {e}")

            current_page += 1
            max_page = data.get("result", {}).get("max_page_no", current_page)
            if current_page > max_page:
                break

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
