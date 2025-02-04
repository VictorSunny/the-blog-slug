from django.contrib import admin
from . models import UserBlog, Category
# Register your models here.
admin.site.register(UserBlog)
admin.site.register(Category)