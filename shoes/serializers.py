from rest_framework import serializers
from shoes.models import Shoe, Brand


class ShoeSerializer(serializers.ModelSerializer):
    qty = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    brand_name = serializers.CharField(max_length=50)

    class Meta:
        model = Shoe
        fields = ('id', 'info', 'name', 'image', 'price', 'sex', 'type', 'brand_name', 'sale', 'views', 'qty', 'size')

    def get_qty(self, obj):
        qty_sizes = obj.qty.all()
        qty_dict = {qty_size.size: qty_size.qty for qty_size in qty_sizes}
        return qty_dict

    def get_size(self, obj):
        qty_sizes = obj.qty.all()
        size_list = [qty_size.size for qty_size in qty_sizes]
        return size_list

class HotDealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoe
        fields = ('id', 'name', 'image', 'price', 'sale')

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('name',)
