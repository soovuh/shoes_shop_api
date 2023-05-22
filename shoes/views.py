from rest_framework.viewsets import ModelViewSet


from shoes.models import Shoe
from shoes.serializers import ShoeSerializer


class ShoeViewSet(ModelViewSet):
    queryset = Shoe.objects.all()
    serializer_class = ShoeSerializer
