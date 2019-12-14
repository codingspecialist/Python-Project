from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from nomadgram2.notifications import views as notification_views

def get_user(username):
    try:
        found_user = models.User.objects.get(username=username)
        return found_user
    except models.User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# 전체 회원 중 최근 가입한 5명 보기
class ExploreUsers(APIView):
    def get(self, request, format=None):
        five_user = models.User.objects.all().order_by('-date_joined')[:5]
        serializer = serializers.ListUserSerializer(five_user, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class UserProfile(APIView):

    # update profile
    def put(self, request, username, format=None):
        user = request.user
        found_user = get_user(username)
        if found_user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif found_user.username != user.username:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            # 부분 업데이트 partial=True
            # 시리얼라이저 인수 = 대상객체, request.data
            serializer = serializers.UserProfileSerializer(found_user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, username, format=None):
        found_user = get_user(username)
        if found_user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.UserProfileSerializer(found_user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class FollowUser(APIView):
    def post(self, request, user_id, format=None):

        from_user = request.user
        
        try:
            to_user = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # add함수 https://milooy.wordpress.com/2016/06/23/django-models-2-making-queries/
        # ManyToMany 필드에서 데이터 추가시에 객체를 add한다.
        from_user.followings.add(to_user)
        to_user.followers.add(from_user)
        from_user.save()
        to_user.save()

        #notifications follow - 여기서 모델 받아와서 작업하는 것 보다 그냥 view불러서 함수 실행이 좋음.
        notification_views.create_notification(from_user, to_user, "follow")
        
        return Response(status=status.HTTP_200_OK)

class UnFollowUser(APIView):
    def post(self, request, user_id, format=None):
        
        from_user = request.user

        try:
            to_user = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        from_user.followings.remove(to_user)
        to_user.followers.remove(from_user)        
        from_user.save()
        to_user.save()

        #notifications follow
        notification_views.delete_notification(from_user, to_user, "follow")        

        return Response(status=status.HTTP_200_OK)

class UserFollowings(APIView):
    def get(self, request, username, format=None):
        found_user = get_user(username)
        followings_list = found_user.followings.all()
        serializer = serializers.ListUserSerializer(followings_list, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class UserFollowers(APIView):
    def get(self, request, username, format=None):
        found_user = get_user(username)
        followers_list = found_user.followers.all()
        serializer = serializers.ListUserSerializer(followers_list, many=True, context={"request":request})

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class Search(APIView):
    def get(self, request, formant=None):
        username = request.query_params.get("username")
        
        if username is not None:
            # 비슷한 이름으로 시작하는 것을 찾으니까 users가 단수 혹은 복수 둘다 가능하다.
            users = models.User.objects.filter(username__istartswith = username)
            serializer = serializers.ListUserSerializer(users, many=True)
            
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ChangePassword(APIView):
    def put(self, request, username, format=None):
        user = request.user

        if user.username != username:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        current_password = request.data.get("current_password",None)
        
        if current_password is not None:
            # base_user.py 가 set_password(), check_password() 가지고 있음.

            if user.check_password(current_password):
                new_password = request.data.get("new_password", None)
                if new_password is not None:
                    user.set_password(new_password)
                    user.save()
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
