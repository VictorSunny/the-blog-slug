from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class UserBlog(models.Model):
    author = models.ForeignKey(User,on_delete= models.CASCADE, related_name= 'user_blogs')
    headline = models.TextField(max_length=255, blank= False)
    category = models.ForeignKey(Category, default=6,on_delete= models.CASCADE, related_name= "user_blogs")
    body = models.TextField(max_length=4000, blank= False)
    source = models.URLField(blank=False, help_text= "Please provide a reputable source for reference")
    date_created = models.DateTimeField(auto_now_add= True)
    date_modified = models.DateTimeField(auto_now= True)

    class Meta:
        ordering = ('-date_created',)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete= models.DO_NOTHING, related_name= 'comments')
    date_created = models.DateTimeField(auto_now_add= True)
    body = models.TextField(max_length= 255, blank= False, help_text= "Enter Comment")
    blog = models.ForeignKey(UserBlog, on_delete= models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['-date_created',]