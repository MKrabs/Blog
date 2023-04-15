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

from blog.presentation.api.like_service import LikeService
from blog.presentation.views.homepage_view import ViewsService as views
from blog.presentation.views.registration_view import RegistrationView
from djangoProject import settings

registration_view = RegistrationView()
liked_view = LikeService()

urlpatterns = [
    path('admin/', admin.site.urls),
    path("me/", include("django.contrib.auth.urls")),
    path("me/register", registration_view.register_page, name='register'),

    # ex: /blog/
    path('', views.index, name='home'),
    path('<int:page>', views.index),
    path('<int:page>/', views.index),
    path('post/<int:post_id>/', views.post, name='post'),
    path('post/<int:post_id>/<int:page>/', views.post),
    path('post/<int:post_id>/liked', views.liked),
    path('post/<int:post_id>/comment', views.comment),
    path('post/<int:post_id>/comment/<int:comm_id>/rm', views.comment_delete),

    path('new/', views.index, name='new'),
    path('create/', views.create_post, name='create'),


    path('@<str:user_name>/', views.user_profile, name='user_profile'),
    path('@<str:user_name>/<str:activity_type>/', views.user_profile, name='user_profile_type'),

    path('', views.page_not_found, name='404'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
