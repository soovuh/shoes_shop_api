import json

from django.contrib.auth.models import User
from django.db.models import Subquery, OuterRef
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from django.urls import reverse

from shoes.models import Brand, QtySize, Shoe
from shoes.serializers import ShoeSerializer, HotDealsSerializer


class ShoeAPITestCase(APITestCase):
    def setUp(self):
        self.maxDiff = None
        self.user = User.objects.create(username='test_user1')
        self.brand_1 = Brand.objects.create(name='Adidas')
        self.brand_2 = Brand.objects.create(name='Reebok')
        self.qty_1 = QtySize.objects.create(qty=6, size=38)
        self.qty_2 = QtySize.objects.create(qty=4, size=39)
        self.qty_3 = QtySize.objects.create(qty=5, size=37)
        self.shoe_1 = Shoe.objects.create(
            info='Some info about shoes, that we see on the product page.',
            name='Reebok Classic',
            image='http://127.0.0.1:8000/media/item_images/Reebok-Classic.jpg',
            type='low-top',
            price='220.00',
            sex='male',
            brand=self.brand_2,
            sale='0.30',
            views=2,
        )
        self.shoe_1.qty.set([self.qty_1, self.qty_2])
        self.shoe_2 = Shoe.objects.create(
            info='Some info about shoes, that we see on the product page.',
            name='Adidas Superstar',
            image='http://127.0.0.1:8000/media/item_images/Adidas-Super-Star.jpg',
            type='low-top',
            price='200.00',
            brand=self.brand_1,
            sex='female',
            sale='0.00',
            views=2,
        )
        self.shoe_2.qty.set([self.qty_3])

    def test_get_shoes(self):
        factory = APIRequestFactory()
        url = '/shoe/'
        request = factory.get(url)
        response = self.client.get(url)
        shoes = Shoe.objects.all().annotate(
            brand_name=Subquery(Brand.objects.filter(pk=OuterRef('brand_id')).values('name')[:1])
        ).prefetch_related('qty')
        serializer_data = ShoeSerializer(shoes, many=True, context={'request': request}).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_hotdeals_shoes(self):
        factory = APIRequestFactory()
        url = '/hotdeals/'
        request = factory.get(url)
        response = self.client.get(url)
        hotdeals = Shoe.objects.order_by('-sale').annotate(
            brand_name=Subquery(Brand.objects.filter(pk=OuterRef('brand_id')).values('name')[:1])
        )[:9]
        serializer_data = HotDealsSerializer(hotdeals, many=True, context={'request': request}).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

