from rest_framework import serializers
from . import models
from nomadgram2.users import models as user_models
from taggit_serializer.serializers import TagListSerializerField

class FeedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.User
        fields = (
            "id",
            "profile_image",
            "username",
            "name",
            "bio",
            "website",
            "followers_count",
            "followings_count"
        )

class CommentSerializer(serializers.ModelSerializer):

    creator = FeedUserSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = (
            "id",
            "message",
            "creator"
        )


class ImageSerializer(serializers.ModelSerializer):

    creator = FeedUserSerializer(read_only=True)
    comments = CommentSerializer(many=True)
    tags = TagListSerializerField()

    class Meta:
        model = models.Image
        fields = (
            "id",
            "file",
            "location",
            "caption",
            "creator", #객체
            "comments", #객체
            "like_count",
            "comment_count",
            "created_at",
            "tags" #객체
        )


class CountImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = (
            "id",
            "file",
            "comment_count",
            "like_count"
        )

class SmallImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = (
            "id",
            "file"
        )

class InputImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = (
            "id",
            "file",
            "location",
            "caption"
        )       