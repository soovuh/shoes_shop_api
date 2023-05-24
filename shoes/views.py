from django.db.models import Subquery, OuterRef
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shoes.models import Shoe, Brand, HomePageCarousel
from shoes.serializers import ShoeSerializer, BrandSerializer, HotDealsSerializer, CarouselSerializer


class ShoeViewSet(ModelViewSet):
    queryset = Shoe.objects.all().annotate(
        brand_name=Subquery(Brand.objects.filter(pk=OuterRef('brand_id')).values('name')[:1])
    ).prefetch_related('qty')
    serializer_class = ShoeSerializer
    # search url looks like this: http://127.0.0.1:8000/shoe/?search=adidas
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'brand_name', 'type', 'info']

    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        shoe = self.get_object()
        shoe.views += 1
        shoe.save()
        return Response({'message': 'Views count incremented'})


class HotDealsView(ModelViewSet):
    queryset = Shoe.objects.order_by('-sale').annotate(
        brand_name=Subquery(Brand.objects.filter(pk=OuterRef('brand_id')).values('name')[:1])
    )[:9]
    serializer_class = HotDealsSerializer



class CarouselView(ModelViewSet):
    queryset = HomePageCarousel.objects.all().order_by('sequence')[:9]
    serializer_class = CarouselSerializer


class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all().values('name')
    serializer_class = BrandSerializer
