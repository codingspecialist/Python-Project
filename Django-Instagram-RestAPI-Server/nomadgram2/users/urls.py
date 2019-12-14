from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("explore/", view=views.ExploreUsers.as_view()),
    path("search/", view=views.Search.as_view()),
    path("<username>/", view=views.UserProfile.as_view()),
    path("<int:user_id>/follow/", view=views.FollowUser.as_view()),
    path("<int:user_id>/unfollow/", view=views.UnFollowUser.as_view()),
    path("<username>/followers/", view=views.UserFollowers.as_view()),
    path("<username>/followings/", view=views.UserFollowings.as_view()),
    path("<username>/password/", view=views.ChangePassword.as_view()),
]
