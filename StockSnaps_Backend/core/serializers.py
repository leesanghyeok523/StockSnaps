from rest_framework import serializers
from .models import Profile, SavingsProduct, Post, Stock, StockReport
from .models import CustomUser

# 프로필 Serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'nickname', 'age', 'income_level']

# 예적금 Serializer
class SavingsProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsProduct
        fields = '__all__'

# 게시판 Serializer
class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content', 'created_at']

# 주식 데이터 Serializer
class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

# 주식 요약 Serializer
class StockReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockReport
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'subscribed_products']

    def to_representation(self, instance):
        """subscribed_products를 쉼표로 구분된 텍스트 대신 리스트로 반환"""
        representation = super().to_representation(instance)
        representation['subscribed_products'] = instance.get_subscribed_products()
        return representation