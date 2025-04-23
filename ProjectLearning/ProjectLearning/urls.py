"""
URL configuration for ProjectLearning project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from . import views
from .views import home, project_detail
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('project/<int:project_id>/', project_detail, name='project_detail'),
    #path('register/', views.register, name='register'),
    #path('login/', views.login, name='login'),
    #path('projects/', views.all_projects_view, name='projects'),
    path('projects/', views.projects_view, name='projects'),
    path('create_project/', views.create_project_view, name='create_project'),
    path('accounts/', include('accounts.urls')),
    path('accounts/register/', auth_views.LoginView.as_view(), name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('project/<int:project_id>/chat/messages/', views.get_chat_messages, name='chat_messages'),
    path('project/<int:project_id>/chat/send/', views.post_chat_message, name='chat_send'),
    path('task/toggle/', views.toggle_task_completion, name='toggle_task_completion'),
    path('project/<int:project_id>/remove_member/', views.remove_member, name='remove_member'),
    path('project/<int:project_id>/invite_member/', views.invite_member, name='invite_member'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
