"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from django.conf.urls.static import static

from blog.presentation.api.like_service import LikeService as liked_view
from blog.presentation.views.homepage_view import HomepageView as homepage_view
from blog.presentation.views.registration_view import RegistrationView as registration_view
from blog.presentation.api.comment_service import CommentService as comment
from blog.presentation.views.profile_view import ProfileView as profile_view
from blog.presentation.views.post_view import PostView as post_view

from djangoProject import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("me/", include("django.contrib.auth.urls")),
    path("me/register", registration_view.register_page, name='register'),

    # ex: /blog/
    path('', homepage_view.index, name='home'),
    path('<int:page>', homepage_view.index),
    path('<int:page>/', homepage_view.index),
    path('post/<int:post_id>/', post_view.post, name='post'),
    path('post/<int:post_id>/<int:page>/', post_view.post),
    path('post/<int:post_id>/liked', liked_view.liked),
    path('post/<int:post_id>/comment', comment.comment),
    path('post/<int:post_id>/comment/<int:comm_id>/rm', comment.comment_delete),

    path('new/', homepage_view.index, name='new'),
    path('create/', post_view.create_post, name='create'),


    path('@<str:user_name>/', profile_view.user_profile, name='user_profile'),
    path('@<str:user_name>/<str:activity_type>/', profile_view.user_profile, name='user_profile_type'),

    path('', homepage_view.page_not_found, name='404'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
