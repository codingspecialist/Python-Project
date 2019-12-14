from django.contrib import admin
from . import models

@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display_links = (
        "creator",
    )

    list_display = (
        "id",
        "creator",
        "to",
        "notification_type"
    )