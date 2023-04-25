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
from django.conf.urls.static import static

from blog.presentation.views.homepage_view import HomepageView as homepage_view
from blog.presentation.views.registration_view import RegistrationView as registration_view

from djangoProject import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("me/", include("django.contrib.auth.urls")),
    path("me/register/", registration_view.register_page, name='register'),

    path('', include('blog.presentation.views.urls')),

    path('api/', include('blog.presentation.api.urls')),

    path('<str:pattern>', homepage_view.page_not_found, name='404'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
