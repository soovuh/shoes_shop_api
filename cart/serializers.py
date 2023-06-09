from rest_framework import serializers

from cart.models import CartItem
from shoes.serializers import ShoeSerializer


class CartItemSerializer(serializers.ModelSerializer):
    shoe = ShoeSerializer()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        shoe_data = data.pop('shoe')
        data.update(shoe_data)
        data['id'] = shoe_data['id']
        return data

    class Meta:
        model = CartItem
        fields = ('id', 'shoe', 'user_size', 'user_qty')
