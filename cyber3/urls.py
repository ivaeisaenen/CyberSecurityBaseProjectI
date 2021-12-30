"""cyber3 URL Configuration

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
from django.urls import path, re_path, include
# from django.contrib.auth.urls
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from messenger import views as messenger_views

favicon_view = RedirectView.as_view(url='/static/images/favicon.png', permanent=True)

urlpatterns = [
    re_path(r'^favicon\.ico$', favicon_view),
    path('admin/', admin.site.urls),
    path('', messenger_views.index, name="index"),
    path('register/', messenger_views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='messenger/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='messenger/logout.html'), name='logout'),
    path('new/', messenger_views.new, name="new"),
    path('send', messenger_views.send, name="send"),
    path('filter_messages_by_user', messenger_views.filter_messages_by_user, name="filter_messages_by_user"),
    path('profile/', messenger_views.profile, name="profile"),
]
