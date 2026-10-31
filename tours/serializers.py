from rest_framework import serializers
from .models import Tours, Review, TourImage, InspiratePlace, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TourImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourImage
        fields = ['id', 'image']

class TourSerializer(serializers.ModelSerializer):
    gallery = TourImageSerializer(many=True, read_only=True)
    category = CategorySerializer(many=True, read_only=True)
    include_list = serializers.SerializerMethodField()
    noinclude_list = serializers.SerializerMethodField()

    class Meta:
        model = Tours
        fields = '__all__'

    def get_include_list(self, obj):
        if obj.include:
            return [line.strip() for line in obj.include.split('\n') if line.strip()]
        return []

    def get_noinclude_list(self, obj):
        if obj.noinclude:
            return [line.strip() for line in obj.noinclude.split('\n') if line.strip()]
        return []

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class InspiratePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspiratePlace
        fields = '__all__'