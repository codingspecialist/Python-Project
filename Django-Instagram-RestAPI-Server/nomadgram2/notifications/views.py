from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers

# 해당클래스의 역할은 자신에게 온 알림 리스트를 보는 것이다. (좋아요, 팔로우, 댓글)
class Notifications(APIView):
    def get(self, request, format=None):
        user = request.user
        notification = models.Notification.objects.filter(to=user)
        serializer = serializers.NotificationSerializer(notification, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

def create_notification(creator, to, notification_type, image=None, comment=None):

    notification = models.Notification.objects.create(
        creator = creator,
        to = to,
        notification_type = notification_type,
        image=image,
        comment=comment
    )
    notification.save()

# 좋아요, 팔로우는 찾아낼 수 있지만, 댓글은 하나의 이미지에 같은 사람이 여러개 달수 있어서 삭제 어려움.
# 나중에 view쪽에서 id로 찾을 수 있을 때 완벽하게 구현하자.
def delete_notification(creator, to, notification_type, image=None):
    # 결과가 하나이면 get, 여러개이면 filter
    try:
        notification = models.Notification.objects.get(
            creator = creator,
            to = to,
            notification_type = notification_type,
            image=image
        )
        notification.delete()
    except models.Notification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

        
