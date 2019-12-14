from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path(
        "users/",
        include("nomadgram2.users.urls", namespace="users")
    ),
    path(
        "accounts/", 
        include("allauth.urls")
    ),
    # namespace를 주면 해당 urls.py에 app_name = images 가 필요함.
    path(
        "images/", 
        include("nomadgram2.images.urls", namespace="images")
    ),
    path(
        "notifications/", 
        include("nomadgram2.notifications.urls", namespace="notifications")
    ),
    path(
        "api-token-auth/", obtain_jwt_token #토큰 생성을 위해
    ),
    path(
        "rest-auth/", include('rest_auth.urls') #로그인, 로그아웃을 위해
    ),
    path(
        "rest-auth/registration/", include('rest_auth.registration.urls') #회원가입을 위해
    ),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
