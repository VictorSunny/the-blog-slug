from django.urls import path, include
from . import views
from authapp.forms import LoginForm

app_name = "core"

urlpatterns = [
    path("", views.home_view, name= 'home'),
    path("create_blog/", views.create_blog_view, name="create_blog"),
    path("blog/<int:pk>/", views.blog_view, name="blog"),
    path("blog/<int:pk>/edit/", views.edit_blog_view, name="edit_blog"),
    path("all_blogs/", views.all_blogs_view, name="all_blogs"),
    path("bookmarks/", views.bookmarked_blogs_view, name= "bookmarked_blogs"),
    path("blog/confirm_delete/<int:blog_id>/", views.confirm_delete_view, name="confirm_delete"),
    path("blog/delete/<int:blog_id>/", views.delete_view, name="delete"),
    path("blog/<int:blog_id>/bookmark/", views.bookmark_view, name= "bookmark"),
    path("comment/delete/<int:pk>/", views.delete_comment_view, name="delete_comment"),
    path("blog/<int:blog_id>/alerts/", views.blog_alert_view, name= "blog_alerts"),
]