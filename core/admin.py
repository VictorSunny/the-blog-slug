from django.contrib import admin
from . models import UserBlog, Category, Notifications
# Register your models here.
admin.site.register(UserBlog)
admin.site.register(Category)
admin.site.register(Notifications)