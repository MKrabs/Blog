from django.urls import path

from blog.presentation.api.post_api import PostAPI
from blog.presentation.api.profile_api import ProfileAPI

urlpatterns = [
    path('index/', PostAPI.get_latest_posts),
    path('post/<int:post_id>/', PostAPI.get_post),

    path('@<str:user_name>/', ProfileAPI.get_user_profile),
]
