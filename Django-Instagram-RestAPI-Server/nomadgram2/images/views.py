from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from nomadgram2.users import serializers as user_serializers
from nomadgram2.users import models as user_models
from nomadgram2.notifications import views as notification_views

# 이미지 찾아주는 함수
def get_image(image_id):
    try:
        found_image = models.Image.objects.get(id=image_id)
        return found_image
    except models.Image.DoesNotExist:
        return None

# https://www.instagram.com/ 으로 가면 친구들의 사진을 볼 수 있다.
# 해당 클래스의 목적은 친구들의 사진을 보는 것이다. 2장씩!! + 내가 올린 사진도 2장만 추가할 것이다.
class Images(APIView):
    def get(self, request, format=None):
        user = request.user

        # followings이 없어도 <QuerySet []> 게 return되기 때문에 null 오류가 없다.
        followings = user.followings.all()[:2]
        
        image_list = []

        for following in followings:
            following_images = following.images.all()[:2]
            for following_image in following_images:
                image_list.append(following_image)
        
        my_images = user.images.all()[:2]
        for my_image in my_images:
            image_list.append(my_image)

        sorted_list = sorted(image_list, key=lambda x:x.created_at, reverse=True)
        serializer = serializers.ImageSerializer(sorted_list, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class LikeImage(APIView):

    # image를 좋아요한 사람들의 리스트를 보고 싶엉ㅎ
    def get(self, request, image_id, format=None):
        found_image = get_image(image_id)
        # 단수일 때는 found_image.creator 가 바로 찾아진다.
        # print(found_image.creator)
        # 결과가 복수일 때는 found_image.likes 이건 바로 안찾아진다. 한건이 아니기 때문이다.
        # 이때는 쿼리셋을 써서 다시 찾아줘야 한다. 
        # 다 찾으려면 found_image.likes.all()
        # 한건만 찾으려면 found_image.likes.get(id=6)
        # 한건만 찾으면 이제 필드명으로 접근이 가능하다. found_image.likes.get(id=6).creator
        
        # 지금 현재 내게 필요한 것은 3번 이미지를 좋아요 한 사람들의 username이나 id이다.
        # 두가지방법이 있다. 첫번째 방법은 for문을 돌리면서 id를 뽑아 내는 것이다.
        # like_creators_ids = []
        # for likes in found_image.likes.all():
        #     print(likes.creator_id) # values()를 호출했을 때 나오는 값으로 바로 호출
        #     print(likes.creator.id) # 객체 한번 더 타서 호출
        #     like_creators_ids.append(likes.creator.id)

        # 아니면 아래와 같이 values()를 이용하는 것이다.
        # print(found_image.likes.all().values())
        like_creators_ids = found_image.likes.values("creator_id")    
        users = user_models.User.objects.filter(id__in = like_creators_ids)
        serializer = user_serializers.ListUserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, image_id, format=None):
        user = request.user

        found_image = get_image(image_id)

        if found_image is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            preexisting_like = models.Like.objects.get(
                creator = user,
                image = found_image    
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Like.DoesNotExist:
            try:
                new_likes = models.Like.objects.create(
                    creator = user,
                    image = found_image
                )
                new_likes.save()
                #notifications like
                notification_views.create_notification(user, found_image.creator, "like", image=found_image)

                return Response(status=status.HTTP_201_CREATED)
            except models.Like.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
    

class UnLikeImage(APIView):
    def delete(self, request, image_id, format=None):
        user = request.user
        found_image = get_image(image_id)
        if found_image is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            preexisting_like = models.Like.objects.get(
                creator = user,
                image = found_image    
            )

            preexisting_like.delete()
            #notifications unlike
            notification_views.delete_notification(user, found_image.creator, "like", image=found_image)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Like.DoesNotExist:
                return Response(status=status.HTTP_304_NOT_MODIFIED) 

class CommentOnImage(APIView):

    def get(self, request, image_id, format=None):
        user = request.user
        found_image = get_image(image_id)
        if found_image is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 댓글을 가져오는 방법 2가지
        # (1) found_image의 related_name으로 가져오기 - 객체에서 가져옴
        comments = found_image.comments.all()
        # (2) comment 모델에서 직접 filter해서 가져오기 - DB에서 가져옴
        #comments = models.Comment.objects.filter(image=found_image)

        # 시리얼 라이즈할 때 객체를 넘기면 인수로 넣고, json을 넘기려면 data=json데이터
        # 만약 json을 넘길 때 다 못넘겼어도 괜찮다. 하지만 save()하려면 
        # 추가적으로 넣어준다. serializer.save(creator=user, image=found_image)
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, image_id, format=None):
        user = request.user
        comment = request.data["message"]
        # comment = 댓글이다
        # request.data = {"message":"댓글이다"}
        
        found_image = get_image(image_id)
        if found_image is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            commentOnImage = models.Comment.objects.create(
                message = comment,
                creator = user,
                image = found_image
            )

            commentOnImage.save()
            #notifications comment
            notification_views.create_notification(user, found_image.creator, "comment", comment=comment)
            return Response(status=status.HTTP_201_CREATED)
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# 내가 적은 댓글 삭제하기
class Comment(APIView):
    def delete(self, request, comment_id, format=None):
        user = request.user
        
        try:
            found_comment = models.Comment.objects.get(id=comment_id)
            if found_comment.creator == user:
                found_comment.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# 내 이미지에 적힌 댓글 삭제하기
class ModerateComment(APIView):
    def delete(self, request, image_id, comment_id, format=None):
        user = request.user

        try:
            found_comment = models.Comment.objects.get(id=comment_id, image__id = image_id, image__creator=user)
            found_comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)         


# 내 이미지에 적힌 댓글 삭제하기 - 내가 만든 버전인데.. 다른 버전을 쓸께!! Join해보자.
# class ModerateComment(APIView):
#     def delete(self, request, image_id, comment_id, format=None):
#         user = request.user
#         try:
#             found_image = get_image(image_id)
#             if found_image.creator == user:
#                 found_comment = models.Comment.objects.get(id=comment_id)
#                 found_comment.delete()
#                 return Response(status=status.HTTP_204_NO_CONTENT)
#             else:
#                 return Response(status=status.HTTP_401_UNAUTHORIZED)
#         except models.Comment.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

# 해쉬태그로 이미지를 찾는 클래스이다.
class Search(APIView):
    def get(self, request, format=None):
        # post로 데이터를 요청받으면 request.data 혹은 request.data["hashtags"]
        # 혹은 request.data.get("hashtags", None)
        # get으로 데이터를 요청받으면 request.query_params.get("hashtags", None)
        hashtags = request.query_params.get("hashtags", None)
        
        if hashtags is not None:
            hashtag_list = hashtags.split(",")

            # tags 는 다운받은 라이브러리다. tags 객체이며 실제로 모델을 가지고 있다. 
            # 해당 모델에 필드는 3개를 가진다. id, name, slug(name을 영어로 변환한 것)
            # tags__name 의 의미는 tags 필드에 조인되어 있는 테이블에 name칼럼에 접근하라는 뜻.
            # __in 은 오른쪽에 대입되는 데이터가 한개가 아니기에 in연산자를 쓴다. 
            # .distinct()를 사용하는 이유는 예를 들어 바다라는 태그로 검색하여 이미지가 3개 검색
            # 되었는데 3개중에 2개가 동일한 이미지라면? 중복을 제거하고 싶다는 뜻이다.
            images = models.Image.objects.filter(tags__name__in = hashtag_list).distinct()
            
            # 이제 이미지를 찾았으니 시리얼라이즈해서 보여주기만 하면 된다.
            # ImageSerializer와 CountImageSrializer 중에 어떤 시리얼을 사용할지는 화면 내용에 따라 다르다.
            serializer = serializers.CountImageSerializer(images, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# get single photo, delete single photo, update single photo
class ImageDetail(APIView):
    def get(self, request, image_id, format=None):
        found_image = get_image(image_id)
        if found_image is None:
            return Response(status=status.HTTP_404_NOT_FOUND)        
        serializer = serializers.ImageSerializer(found_image)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, image_id, format=None):
        user = request.user
        found_image = get_image(image_id)
        if found_image is None:
            return Response(status=status.HTTP_404_NOT_FOUND)    
        if user == found_image.creator:
            found_image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, image_id, format=None):
        user = request.user
        found_image = get_image(image_id)
        if found_image is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if user == found_image.creator:
            # 데이터 변경시에는 data=request.data만 넣어주면 된다.(보낼떄는 json으로 보내면 됨)
            # 모든 데이터가 아니라 부분데이터를 변경하려면 partial=True를 해줘야 한다.
            serializer = serializers.InputImageSerializer(found_image, data=request.data, partial=True)
            # serializer에 데이터를 보내면서 직렬화 하고 바로 save()하면 db에 반영된다.
            # data를 deserializing 할 때, instance를 저장하기 전항상 is_valid()를 호출해야함
            # 에러가 발생하면 .errors로 에러 메세지 호출 가능. {'field name': ['error message']} 형식으로.
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)