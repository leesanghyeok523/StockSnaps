from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Stock
from core.serializers import StockSerializer

@api_view(['GET'])
def stock_summary(request):
    stocks = Stock.objects.all()
    serializer = StockSerializer(stocks, many=True)
    return Response(serializer.data)
