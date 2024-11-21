from rest_framework import serializers
from .models import User, FinancialInstitution, SavingsProduct, DepositProduct, StockBoard, Comment, Image, RealAsset, Interest

# 사용자 Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'joined_products']

    def update(self, instance, validated_data):
            # joined_products가 쉼표로 구분된 문자열로 저장되는지 처리
            joined_products = validated_data.get('joined_products')
            if isinstance(joined_products, list):
                instance.joined_products = ','.join(map(str, joined_products))
            else:
                instance.joined_products = joined_products
            instance.save()
            return instance
# 금융기관 Serializer
class FinancialInstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialInstitution
        fields = ['id', 'institution_code', 'institution_name', 'region', 'phone_number']

# 예금 상품 Serializer
class SavingsProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsProduct
        fields = '__all__'

# 적금 상품 Serializer
class DepositProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = '__all__'  # 또는 명시적으로 필드 정의

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'uploaded_at']

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'content', 'created_at']

class StockBoardSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    author_username = serializers.ReadOnlyField(source='author.username')
    like_count = serializers.ReadOnlyField()

    class Meta:
        model = StockBoard
        fields = ['id', 'title', 'content', 'stock_name', 'created_at', 'updated_at', 
                  'author', 'author_username', 'likes', 'like_count', 'comments', 'images']
        
class RealAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealAsset
        fields = ['id', 'category', 'name', 'value', 'created_at']

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'category', 'item_id', 'liked_at']