from django.urls import path
from . import views

app_name = "images"
urlpatterns = [
    path("", view=views.Images.as_view()),
    path("<int:image_id>/", view=views.ImageDetail.as_view()),
    path("<int:image_id>/likes/", view=views.LikeImage.as_view()),
    path("<int:image_id>/unlikes/", view=views.UnLikeImage.as_view()),
    path("<int:image_id>/comments/", view=views.CommentOnImage.as_view()),
    path("comments/<int:comment_id>/", view=views.Comment.as_view()), # delete i created / comment
    path("<int:image_id>/comments/<int:comment_id>/", view=views.ModerateComment.as_view()), # delete my photo / comment
    path("search/", view=views.Search.as_view()),
    
]
