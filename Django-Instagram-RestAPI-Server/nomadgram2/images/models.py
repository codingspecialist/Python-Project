from django.db import models
from nomadgram2.users import models as user_models
from django.utils.encoding import python_2_unicode_compatible
from taggit.managers import TaggableManager

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add = True) # 현재시간 추가
    updated_at = models.DateTimeField(auto_now = True) # 현재시간 업데이트

    # Meta 클래스는 내부 클래스이다.
    # Meta 클래스의 주 목적은 클래스가 만들어질 때 클래스를 자동으로 바꾸기 위한 것.
    # 
    class Meta:
        # 추상클래스라고 선언
        abstract = True

@python_2_unicode_compatible
class Image(TimeStampedModel):
    file = models.ImageField()
    location = models.CharField(max_length=140)
    caption = models.TextField()
    # 참조된 User객체가 삭제될 때 image가 함께 삭제된다. on_delete=models.CASCADE
    creator = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="images")
    # https://django-taggit.readthedocs.io/en/latest/getting_started.html
    # pipenv install django-taggit
    # python manage.py migrate -> db에 tag 테이블 생성됨.
    # base.py -> TAGGIT_CASE_INSENSITIVE = True
    # THIRD_PARTY_APPS -> taggit 등록
    tags = TaggableManager()

    # 연관 필드명
    # (1) likes
    # (2) comments

    @property
    def like_count(self):
        return self.likes.all().count()

    @property
    def comment_count(self):
        # related_name이 없으면 self.comment_set.all().count()
        return self.comments.all().count()

    def __str__(self):
        return "{}".format(self.caption)

    # 이미지 생성순으로 order by 하기
    class Meta:
        ordering = ["-created_at"]


# related_name 을 사용하면 Image에서 Like를 찾아야 할 때!! 
# Like_set.all() 이렇게 안쓰고 likes.all()로 찾을 수 있다.
class Like(TimeStampedModel):
    creator = models.ForeignKey(user_models.User, on_delete=models.CASCADE, null=True)
    # Image.objects.get(id=1).likes.all()
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, related_name="likes")

    def __str__(self):
        return "User: {} - Image Caption: {}".format(self.creator.username, self.image.caption)

class Comment(TimeStampedModel):
    message = models.TextField()
    # related_name 이 없을 때는 아래처럼 한다.
    # Image.objects.get(id=1).comment_set.all()

    # User에 creator가 있기 때문에 related_name이 필요없다. 없을 때 적어주는 거다. set안쓰려고!
    creator = models.ForeignKey(user_models.User, on_delete=models.CASCADE, null=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, related_name="comments")

    def __str__(self):
        return self.message