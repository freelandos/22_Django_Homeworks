from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favourite
from advertisements.permissions import IsOwnerOrIsAdmin
from advertisements.serializers import AdvertisementSerializer, FavouriteSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrIsAdmin()]
        return []

    def list(self, request, *args, **kwargs):
        try:
            status_queryset = Advertisement.objects.all().exclude(~Q(creator=request.user), status="DRAFT")
            queryset = self.filter_queryset(status_queryset)
            serializer = AdvertisementSerializer(queryset, many=True)
        except TypeError:
            status_queryset = Advertisement.objects.all().exclude(status="DRAFT")
            queryset = self.filter_queryset(status_queryset)
            serializer = AdvertisementSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def add_favorite(self, request, pk=None):
        advertisement = self.get_object()
        user = self.request.user
        if not user.is_authenticated:
            return Response({"detail": "You must be logged in to add favorites."})
        if user == advertisement.creator:
            return Response({"detail": "You can't add your own advertisement to favorites."})
        favorite = Favourite.objects.create(user=user, advertisement=advertisement)
        serializer = FavouriteSerializer(favorite)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def get_favorites(self, request, pk=None):
        user = self.request.user
        if not user.is_authenticated:
            return Response({"detail": "You must be logged in to get favorites."})
        favorites = Favourite.objects.filter(user=user)
        serializer = FavouriteSerializer(favorites, many=True)
        return Response(serializer.data)
