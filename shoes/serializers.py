from rest_framework import serializers
from shoes.models import Shoe, Brand, HomePageCarousel, QtySize


class QtySizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QtySize
        fields = ('size', 'qty', 'shoe')


class ShoeSerializer(serializers.ModelSerializer):
    sizes = QtySizeSerializer(many=True, read_only=True)
    brand_name = serializers.CharField(source='brand.name', max_length=50)

    class Meta:
        model = Shoe
        fields = ('id', 'info', 'name', 'image', 'price', 'sex', 'type', 'brand_name', 'sale', 'views', 'sizes')


class HotDealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoe
        fields = ('id', 'name', 'image', 'price', 'sale')


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('name',)


class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePageCarousel
        fields = ('image', 'sequence')
