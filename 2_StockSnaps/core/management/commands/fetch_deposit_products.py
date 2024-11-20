import requests
from django.core.management.base import BaseCommand
from core.models import DepositProduct
from decouple import config

class Command(BaseCommand):
    help = "Fetch deposit products from external API and save them to the database."

    def handle(self, *args, **kwargs):
        url = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"
        api_key = config('FSS_API_KEY')

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
                    self.stdout.write(f"Created: {obj.financial_product_name}")
                else:
                    self.stdout.write(f"Skipped: {obj.financial_product_name}")

            current_page += 1
            max_page = data.get("result", {}).get("max_page_no", current_page)
            if current_page > max_page:
                break
