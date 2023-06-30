import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status
from rest_framework.decorators import action

from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.db.utils import IntegrityError

from accounts.models import Address
from cart.models import Cart
from orders.models import Order, OrderItem, OrderAddress


class OrderViewSet(viewsets.ViewSet):
    @csrf_exempt
    @action(detail=False, methods=['post'])
    def create_order(self, request):
        session_id = request.COOKIES.get('sessionid')

        try:
            session = Session.objects.get(session_key=session_id)
        except Session.DoesNotExist:
            return JsonResponse({'message': 'Session not fonud'}, status=404)

        user_id = session.get_decoded().get('_auth_user_id')

        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
            previous_address = user.address
            phone_number = request.data.get('phone_number')
            total = request.data.get('total')
            city = request.data.get('city')
            street = request.data.get('street')
            postcode = request.data.get('postcode')

            if phone_number:
                try:
                    try:
                        phone_used = User.objects.get(phone_number=phone_number)
                        if phone_used != user:
                            return JsonResponse({'message': "Phone already used"})
                    except ObjectDoesNotExist:
                        user.phone_number = phone_number
                        user.save()
                except IntegrityError:
                    return JsonResponse({'message': "Phone already used"})
            if city and street and postcode:
                city = city.capitalize()
                street = street.capitalize()

                try:
                    address = Address.objects.get(city=city, street=street, postcode=postcode)
                except Address.DoesNotExist:
                    address = Address.objects.create(city=city, street=street, postcode=postcode)
                    address.save()
                user.address = address
                user.save()
                if User.objects.filter(address=previous_address).aggregate(count=Count('id'))['count'] < 1:
                    previous_address.delete()
            order_address = OrderAddress.objects.create(city=address.city, postcode=address.postcode,
                                                        street=address.street)
            cart = Cart.objects.get(user=user)
            if len(cart.cartitem_set.all()) <= 0:
                return JsonResponse({"message": "Cart is empty!"})
            order = Order.objects.create(user=user, address=order_address, total=total,
                                         name=f'{uuid.uuid4().hex[:6]}')

            for item in cart.cartitem_set.all():
                order_item = OrderItem.objects.create(order=order, shoe=item.shoe, user_size=item.user_size,
                                                      user_qty=item.user_qty)
                order.shoes.add(item.shoe)
                order.save()
                order_item.save()
            order.save()
            for item in cart.cartitem_set.all():
                item.delete()
            cart.save()
            return JsonResponse({"message": "Order created"})
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)
