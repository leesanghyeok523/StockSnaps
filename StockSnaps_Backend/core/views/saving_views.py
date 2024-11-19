import requests
from django.http import JsonResponse
from core.models import SavingsProduct

# 데이터 검증 함수
def validate_numeric(value, default=0.0):
    try:
        return float(value)  # 숫자로 변환
    except (ValueError, TypeError):
        return default  # 변환 실패 시 기본값 반환

def fetch_and_store_savings_products(request):
    API_URL = "https://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"
    API_KEY = "YOUR_API_KEY"  # 환경 변수에서 불러오는 것이 권장
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000',  # 금융 그룹 코드 (은행)
        'pageNo': 1,
    }

    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        products = response.json()
        print("API Response:", products)  # 전체 API 응답 출력
        products = products.get('result', {}).get('baseList', [])
        print("Parsed Products:", products)  # 파싱된 데이터 출력
        saved_count = 0
        skipped_count = 0

        for product in products:
            try:
                obj, created = SavingsProduct.objects.get_or_create(
                    bank_name=product['kor_co_nm'],
                    product_name=product['fin_prdt_nm'],
                    term=product.get('join_deny', 0),
                    defaults={
                        'interest_rate': validate_numeric(product.get('intr_rate', 0)),
                        'preferential_rate': validate_numeric(product.get('intr_rate2', 0)),
                        'min_amount': validate_numeric(product.get('join_member', 0)),
                        'max_amount': validate_numeric(product.get('join_deny', 0)),
                        'rate_type': product.get('rate_type', ''),
                        'join_conditions': product.get('etc_note', ''),
                    }
                )
                if created:
                    saved_count += 1
                else:
                    skipped_count += 1
            except Exception as e:
                # 오류가 발생한 항목은 건너뜀
                print(f"Error saving product: {product}. Error: {e}")
                skipped_count += 1

        return JsonResponse({
            'message': 'Data fetching complete.',
            'saved': saved_count,
            'skipped': skipped_count,
        })

    return JsonResponse({'error': 'Failed to fetch data from API.'}, status=500)
