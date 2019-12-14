from rest_framework import serializers
from . import models
from nomadgram2.images import serializers as images_serializers

class UserProfileSerializer(serializers.ModelSerializer):

    images = images_serializers.CountImageSerializer(many=True, read_only=True)
    post_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    followings_count = serializers.ReadOnlyField()

    class Meta:
        model = models.User
        fields = (
            "id",
            "profile_image",
            "username",
            "name",
            "bio",
            "website",
            "post_count",
            "followers_count",
            "followings_count",
            "images"
        )

class ListUserSerializer(serializers.ModelSerializer):

    followings = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = (
            "id",
            "profile_image",
            "username",
            "name",
            "bio",
            "website",
            "post_count",
            "followers_count",
            "followings_count",
            "followings"
        )

    # obj 는 현재 시리얼 라이즈 객체 (1개)
    def get_followings(self, obj):
        if "request" in self.context:
            request = self.context["request"]

            # 현재 시리얼 라이즈 객체 obj와 내가 followings하고 있는 List를 모두 비교해준다.
            # list = ["a","b","c"]
            # if "a" in list: 이것의 의미는 list 배열 3개중에 a가 있느냐를 판단해서 boolean을 리턴한다.
            if obj in request.user.followings.all():
                return True
        return False

        # 추가 설명 자바로 말하자면 if in문법은 contains함수와 동일하다.
        """
            ArrayList<String> pocket = new ArrayList<String>();
            pocket.add("paper");
            pocket.add("handphone");
            pocket.add("money");

            if (pocket.contains("money")) {
                System.out.println("택시를 타고 가라");
            }else {
                System.out.println("걸어가라");
            }
        """