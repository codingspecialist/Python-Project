from django.db import models
from nomadgram2.users import models as user_models
from nomadgram2.images import models as image_models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Notification(image_models.TimeStampedModel):
    TYPE_CHOICES = (
        ("like","Like"),
        ("comment", "Comment"),
        ("follow", "Follow")
    )

    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, related_name="creator") 
    to = models.ForeignKey(user_models.User, on_delete=models.PROTECT, related_name="to") 
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    image = models.ForeignKey(image_models.Image, on_delete=models.PROTECT, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return "From: {} - To: {} - Type: {}".format(self.creator, self.to, self.notification_type)