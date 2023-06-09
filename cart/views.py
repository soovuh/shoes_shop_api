from django.contrib.auth import get_user_model
from django.db.models import Subquery, OuterRef
from django.contrib.sessions.models import Session
from rest_framework.viewsets import ModelViewSet

from cart.models import CartItem
from cart.serializers import CartItemSerializer
from shoes.models import Shoe, Brand


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
            brand_name=Subquery(Brand.objects.filter(pk=OuterRef('shoe__brand_id')).values('name')[:1])
            ).prefetch_related('shoe__qty')

