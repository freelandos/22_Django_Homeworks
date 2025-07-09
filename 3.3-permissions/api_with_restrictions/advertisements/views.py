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
        elif self.action in ["add_favorite", "get_favorites"]:
            return [IsAuthenticated()]
        return []

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Advertisement.objects.all()
        elif user.is_authenticated:
            return Advertisement.objects.exclude(
                Q(status="DRAFT") & ~Q(creator=user)
            )
        else:
            return Advertisement.objects.exclude(
                Q(status="DRAFT")
            )

    @action(detail=True, methods=["post"])
    def add_favorite(self, request, pk=None):
        advertisement = self.get_object()
        user = self.request.user
        if user == advertisement.creator:
            return Response(
                {"detail": "You can't add your own advertisement to favorites."},
                status=400
            )
        if Favourite.objects.filter(user=user, advertisement=advertisement).exists():
            return Response(
                {"detail": "This advertisement is already in favorites."},
                status=400
            )
        favorite = Favourite.objects.create(user=user, advertisement=advertisement)
        serializer = FavouriteSerializer(favorite)
        return Response(serializer.data, status=201)

    @action(detail=False, methods=["get"])
    def get_favorites(self, request):
        user = self.request.user
        favorites = Favourite.objects.filter(user=user)
        serializer = FavouriteSerializer(favorites, many=True)
        return Response(serializer.data, status=200)
