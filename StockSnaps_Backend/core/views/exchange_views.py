import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def exchange_rate(request):
    from_currency = request.data.get('from_currency')
    to_currency = request.data.get('to_currency')
    response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency}")
    rate = response.json().get('rates', {}).get(to_currency, None)
    return Response({'rate': rate})
