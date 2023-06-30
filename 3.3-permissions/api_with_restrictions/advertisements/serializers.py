from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, Favourite


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        if data.get('status') in ['CLOSED', 'DRAFT']:
            return data
        if Advertisement.objects.filter(status='OPEN', creator=self.context['request'].user).count() >= 10:
            raise serializers.ValidationError('Exceeded allowed number of open ads.')
        return data


class FavouriteSerializer(serializers.ModelSerializer):
    """Serializer для избранного."""

    user = UserSerializer()
    advertisement = AdvertisementSerializer()

    class Meta:
        model = Favourite
        fields = ['id', 'user', 'advertisement']
