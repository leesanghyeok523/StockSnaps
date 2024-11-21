import requests
from django.core.management.base import BaseCommand
from core.models import Exchange
from decouple import config

class Command(BaseCommand):
    help = "Fetch exchange rates from Korea EximBank API and save them to the database."

    def handle(self, *args, **kwargs):
        url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
        api_key = config('EXCHANGE_RATE_API_KEY')  # 환경변수에서 API 키 가져오기

        if not api_key:
            self.stderr.write("EXIMBANK_API_KEY is not set in the environment variables.")
            return

        params = {
            "authkey": api_key,
            "searchdate": "20241121",  # 오늘 날짜를 하드코딩 (테스트용)
            "data": "AP01"
        }

        response = requests.get(url, params=params)
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

        if not data:
            self.stderr.write("No exchange rate data returned.")
            return

        # 데이터 처리
        for item in data:
            try:
                obj, created = Exchange.objects.update_or_create(
                    cur_unit=item.get("cur_unit", "Unknown"),
                    defaults={
                        "cur_nm": item.get("cur_nm", "Unknown"),
                        "ttb": self.parse_decimal(item.get("ttb")),
                        "tts": self.parse_decimal(item.get("tts")),
                        "deal_bas_r": self.parse_decimal(item.get("deal_bas_r")),
                        "bkpr": self.parse_decimal(item.get("bkpr")),
                        "yy_efee_r": self.parse_decimal(item.get("yy_efee_r")),
                        "ten_dd_efee_r": self.parse_decimal(item.get("ten_dd_efee_r")),
                        "kftc_deal_bas_r": self.parse_decimal(item.get("kftc_deal_bas_r")),
                        "kftc_bkpr": self.parse_decimal(item.get("kftc_bkpr")),
                    }
                )
                if created:
                    self.stdout.write(f"Created: {obj.cur_nm}")
                else:
                    self.stdout.write(f"Updated: {obj.cur_nm}")
            except Exception as e:
                self.stderr.write(f"Error saving exchange rate for {item.get('cur_nm', 'Unknown')}: {e}")

    def parse_decimal(self, value):
        """Convert string to Decimal if possible, otherwise return None."""
        try:
            if value is not None:
                return float(value.replace(",", ""))
        except (ValueError, AttributeError):
            return None