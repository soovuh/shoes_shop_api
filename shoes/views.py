from django.db.models import Subquery, OuterRef
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shoes.models import Shoe, Brand
from shoes.serializers import ShoeSerializer, BrandSerializer


class ShoeViewSet(ModelViewSet):
    queryset = Shoe.objects.all().annotate(
        brand_name=Subquery(Brand.objects.filter(pk=OuterRef('brand_id')).values('name')[:1])
    ).prefetch_related('qty')
    serializer_class = ShoeSerializer

    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        shoe = self.get_object()
        shoe.views += 1
        shoe.save()
        return Response({'message': 'Views count incremented'})


class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all().values('name')
    serializer_class = BrandSerializer


