import json

from django.contrib.auth import get_user_model
from django.db.models import Subquery, OuterRef
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.views import View
from rest_framework.viewsets import ModelViewSet

from cart.models import CartItem, Cart
from cart.serializers import CartItemSerializer
from shoes.models import Shoe, QtySize


class CartViewSet(ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        session_id = self.request.COOKIES.get('sessionid')

        try:
            session = Session.objects.get(session_key=session_id)
        except Session.DoesNotExist:
            return CartItem.objects.none()

        user_id = session.get_decoded().get('_auth_user_id')
        User = get_user_model()

        return CartItem.objects.filter(cart__user_id=user_id).annotate(
            brand_name=Subquery(Shoe.objects.filter(pk=OuterRef('shoe_id')).values('brand__name')[:1])
        ).prefetch_related('shoe__sizes')


class CartItemAddView(View):
    def post(self, request):
        session_id = self.request.COOKIES.get('sessionid')
        User = get_user_model()
        try:
            session = Session.objects.get(session_key=session_id)
        except Session.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)
        try:
            user_id = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)
        user_cart = Cart.objects.get(user=user)
        request_data = json.loads(request.body)
        shoe_id = request_data.get('shoe_id')
        user_size = request_data.get('user_size')
        shoe = Shoe.objects.get(pk=shoe_id)
        sizes = QtySize.objects.filter(shoe=shoe, size=user_size)[0]
        if sizes.qty == 0:
            return JsonResponse({'message': 'This size is out!'})
        sizes.qty = sizes.qty - 1
        sizes.save()
        shoe.save()
        try:
            cart_item = user_cart.cartitem_set.get(shoe=shoe, user_size=user_size)
            cart_item.user_qty += 1
            cart_item.save()
            user_cart.save()
            return JsonResponse({'message': 'Change obj in the Cart!'}, status=200)
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(shoe=shoe, cart=user_cart, user_size=user_size, user_qty=1)
            user_cart.shoes.add(shoe)
            cart_item.save()
            user_cart.save()
            return JsonResponse({'message': 'Added to Cart!'}, status=200)