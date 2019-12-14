from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from nomadgram2.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        ("User", {
            "fields": (
                "name",
                "followers",
                "followings"
            ),
        }),
    ) + auth_admin.UserAdmin.fieldsets
    
    list_display_links = (
        "username",
    )
    list_display = ["id","username", "name", "email", "is_superuser"]
    search_fields = ["name"]