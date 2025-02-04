from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views
from .forms import LoginForm

app_name = "core"

urlpatterns = [
    path("", views.homeview, name= 'home'),
    path('signup/', views.signupview, name= 'signup'),
    path("login/", auth_views.LoginView.as_view(authentication_form= LoginForm, template_name= 'login.html'), name= 'login'),
    path("logout/", views.logoutview, name= 'logout'),
    path("profile/", views.dashboard, name= "profile"),
    path("user/<int:pk>/", views.profileview, name= "profile-specific"),
    path("create_blog/", views.createblogview, name="createblog"),
    path("blog/<int:pk>/edit/", views.editblogview, name="editblog"),
    path("blog/<int:pk>/", views.blogview, name="blog"),
    path("all-blogs/", views.allblogsview, name="all-blogs"),
    path("blog/delete/<int:pk>/", views.deleteview, name="delete"),
    path("comment/delete/<int:pk>/", views.deletecommentview, name="deletecomment"),
]