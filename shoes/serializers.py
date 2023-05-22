from rest_framework import serializers
from shoes.models import Shoe, QtySize


class QtySizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QtySize
        fields = ('size', 'qty')


class ShoeSerializer(serializers.ModelSerializer):
    qty = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()

    class Meta:
        model = Shoe
        fields = ('id', 'info', 'href', 'image', 'price', 'sex', 'type', 'brand', 'sale', 'views', 'qty', 'size')

    def get_qty(self, obj):
        qty_sizes = QtySize.objects.filter(shoe=obj)
        qty_dict = {qty_size.size: qty_size.qty for qty_size in qty_sizes}
        return qty_dict

    def get_size(self, obj):
        qty_sizes = QtySize.objects.filter(shoe=obj)
        size_list = [qty_size.size for qty_size in qty_sizes]
        return size_list
