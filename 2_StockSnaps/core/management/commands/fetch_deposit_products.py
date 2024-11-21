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

            # Process baseList (basic product data)
            base_list = data.get("result", {}).get("baseList", [])
            for base in base_list:
                product, created = DepositProduct.objects.get_or_create(
                    financial_company_code=base.get("fin_co_no", "Unknown"),
                    financial_product_code=base.get("fin_prdt_cd", "Unknown"),
                    defaults={
                        "financial_product_name": base.get("fin_prdt_nm", "Unknown"),
                        "join_way": base.get("join_way", "N/A"),
                        "interest_rate_type": None,
                        "interest_rate_type_name": None,
                        "basic_interest_rate": None,
                        "max_interest_rate": None,
                    },
                )
                if created:
                    self.stdout.write(f"Created: {product.financial_product_name}")
                else:
                    self.stdout.write(f"Skipped: {product.financial_product_name}")

            # Process optionList (detailed rate data)
            option_list = data.get("result", {}).get("optionList", [])
            for option in option_list:
                product_code = option.get("fin_prdt_cd")
                deposit_product = DepositProduct.objects.filter(financial_product_code=product_code).first()

                if deposit_product:
                    deposit_product.interest_rate_type = option.get("intr_rate_type", "N/A")
                    deposit_product.interest_rate_type_name = option.get("intr_rate_type_nm", "N/A")
                    deposit_product.basic_interest_rate = option.get("intr_rate", 0.0)
                    deposit_product.max_interest_rate = option.get("intr_rate2", 0.0)
                    deposit_product.save()

                    self.stdout.write(
                        f"Updated: {deposit_product.financial_product_name} - "
                        f"Basic Rate: {deposit_product.basic_interest_rate}, Max Rate: {deposit_product.max_interest_rate}"
                    )

            # Check if more pages exist
            current_page += 1
            max_page = data.get("result", {}).get("max_page_no", current_page)
            if current_page > max_page:
                break
