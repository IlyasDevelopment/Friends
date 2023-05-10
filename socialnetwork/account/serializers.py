from rest_framework import serializers

from .models import User, FriendRequest


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)


class FriendRequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('id', 'from_user', 'to_user')
