from django.contrib.auth.models import AbstractUser
from django.db import models

# PK 설정
# 모델 객체에 primary key 필드값을 변경하고 저장하는 경우, 
# 기존 모델 객체의 primary key 필드값이 바뀌는 것이 아니라, 새로운 모델 객체가 생성됩니다. 
# 물론 기존의 모델객체는 DB상에서 지워지지 않습니다.
# 예 : name = models.CharField(max_length=100, primary_key=True)

# verbose 설정 = 읽기좋은 형태의 필드이름
# first_name = models.CharField("person's first name", max_length=30)

# migrate 오류날 때 "Table 'django_content_type' already exists"
# python manage.py migrate --fake

class User(AbstractUser):

    # enum과 같이 필드에 저장할 수 있는 값이 제한적인 경우에 사용할 수 있습니다. 
    # 옵션값은 아래와 같이 2중 튜플(또는 리스트)로 설정해야합니다.
    # 튜플은 2개의 요소를 가지는데 하나는 실제 DB에 저장될 값
    # 두번째는 admin페이지나 폼에서 표시할 이름
    GENDER_CHOICES = (
        ("male","Male"),
        ("female", "Female"),
        ("not-specified", "Not specified")
    )    

    profile_image = models.ImageField(null=True)
    name = models.CharField(blank=True, max_length=255)
    website = models.URLField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=140, null=True)
    gender = models.CharField(max_length=80, choices=GENDER_CHOICES, null=True)
    # 대칭 테이블이 아닌 자신을 참조하는 테이블임을 선언할 때 symmetrical=False 사용
    # 참고 https://github.com/stardustrain/w_keuntaek_han/blob/master/Class/week4/django_day03.md
    followers = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="user_followings")
    followings = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="user_followers") #ManyToMany 필드를 복수로 이름 짓기!!

    # 연관 필드명
    # (1) images
    # (2) comments
    # (3) creator

    # ManyToOne -> FK설정하면 됨.
    # ManyToMany -> models.ManyToManyField(Topping) -> Topping은 클래스명, 자기자신은 "self"
    # 혹은 자기자신은 아직 객체 생성 이전이기 때문에 문자열로 전달 가능 "User"

    # ManyToMany 필드는 실제로 DB에 새로운 테이블이 생성된다. 이것을 중간 모델(intermediate)이라고 한다.
    # 여기에 추가적인 필드가 필요할 수 있다. 가령 followers 한 시간을 추가한다면?
    # 중간 모델을 직접 선언하려면? https://brunch.co.kr/@ddangdol/6
    '''
        class User(AbstractUser):
            followers = models.ManyToManyField(
                            "self", 
                            through='User_Followers',
                            through_fields=("from_user","to_user"),
                            blank=True,
                            symmetrical=False
                        )

        class Followers(models.Model):
            from_user_id = models.ForeignKey(User)
            to_user_id = models.ForeignKey(User)
            created_at = models.DateTimeField(auto_now_add = True) # 현재시간 추가
    '''

    def __str__(self):
        # username 은 AbstractUser에서 상속받고 있음.
        return self.username

    @property
    def post_count(self):
        # image 모델 생성 후 작업
        pass
    
    @property
    def followers_count(self):
        return self.followers.all().count()

    @property
    def followings_count(self):
        return self.followings.all().count()