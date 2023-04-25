from django.urls import path

from blog.presentation.views.homepage_view import HomepageView
from blog.presentation.views.post_view import PostView
from blog.presentation.views.profile_view import ProfileView

from blog.presentation.api.comment_service import CommentService
from blog.presentation.api.like_service import LikeService

urlpatterns = [
    path('', HomepageView.index, name='home'),
    path('<int:page>/', HomepageView.index),

    path('post/<int:post_id>/', PostView.post, name='post'),
    path('post/<int:post_id>/<int:page>/', PostView.post),
    path('post/<int:post_id>/liked', LikeService.liked),
    path('post/<int:post_id>/comment', CommentService.comment),
    path('post/<int:post_id>/comment/<int:comm_id>/rm', CommentService.comment_delete),

    path('new/', HomepageView.index, name='new'),
    path('create/', PostView.create_post, name='create'),


    path('@<str:user_name>/', ProfileView.user_profile, name='user_profile'),
    path('@<str:user_name>/<str:activity_type>/', ProfileView.user_profile, name='user_profile_type'),
]