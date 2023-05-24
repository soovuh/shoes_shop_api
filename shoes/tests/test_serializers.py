import json

from django.contrib.auth.models import User
from django.db.models import Subquery, OuterRef
from django.test.testcases import TestCase

from shoes.models import Shoe, QtySize, Brand
from shoes.serializers import ShoeSerializer, HotDealsSerializer


class ShoeSerializerTestCase(TestCase):
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

    def test_ok(self):
        shoes = Shoe.objects.all().annotate(
            brand_name=Subquery(Brand.objects.filter(pk=OuterRef('brand_id')).values('name')[:1])
        ).prefetch_related('qty')

        data = ShoeSerializer(shoes, many=True).data
        data = json.loads(json.dumps(data))

        expected_data = [
            {
                "id": self.shoe_1.id,
                "info": "Some info about shoes, that we see on the product page.",
                "name": "Reebok Classic",
                "image": "/media/http%3A/127.0.0.1%3A8000/media/item_images/Reebok-Classic.jpg",
                "price": "220.00",
                "sex": "male",
                "type": "low-top",
                "brand_name": "Reebok",
                "sale": "0.30",
                "views": 2,
                "qty": {"38": 6, "39": 4},
                "size": [38, 39]
            },
            {
                "id": self.shoe_2.id,
                "info": "Some info about shoes, that we see on the product page.",
                "name": "Adidas Superstar",
                "image": "/media/http%3A/127.0.0.1%3A8000/media/item_images/Adidas-Super-Star.jpg",
                "price": "200.00",
                "sex": "female",
                "type": "low-top",
                "brand_name": "Adidas",
                "sale": "0.00",
                "views": 2,
                "qty": {'37': 5},
                "size": [37]
            }
        ]
        self.assertEqual(expected_data, data)


class HotDealsSerializerTestCase(TestCase):
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

    def test_ok(self):
        hotdeals = Shoe.objects.order_by('-sale').annotate(
            brand_name=Subquery(Brand.objects.filter(pk=OuterRef('brand_id')).values('name')[:1])
        )[:9]

        data = HotDealsSerializer(hotdeals, many=True).data
        data = json.loads(json.dumps(data))

        expected_data = [
            {
                "id": self.shoe_1.id,
                "name": "Reebok Classic",
                "image": "/media/http%3A/127.0.0.1%3A8000/media/item_images/Reebok-Classic.jpg",
                "price": "220.00",
                "sale": "0.30",

            },
            {
                "id": self.shoe_2.id,
                "name": "Adidas Superstar",
                "image": "/media/http%3A/127.0.0.1%3A8000/media/item_images/Adidas-Super-Star.jpg",
                "price": "200.00",
                "sale": "0.00",
            }
        ]
        self.assertEqual(expected_data, data)
