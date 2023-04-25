from django.urls import path, include

from blog.presentation.api.post_api import PostAPI

urlpatterns = [
    path('index', PostAPI.get_latest_posts),
    
    path('post/<int:post_id>', PostAPI.get_post),

    path('@<str:user_name>', PostAPI.get_user_profile),
]