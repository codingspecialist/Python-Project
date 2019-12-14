from rest_framework import serializers
from . import models
from nomadgram2.images import serializers as image_serializers
from nomadgram2.users import serializers as user_serializers

class NotificationSerializer(serializers.ModelSerializer):

    # creator
    creator = user_serializers.ListUserSerializer()
    # image
    image = image_serializers.SmallImageSerializer()

    class Meta:
        model = models.Notification
        fields = "__all__"
    