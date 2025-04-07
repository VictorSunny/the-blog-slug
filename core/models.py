from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

class Category(models.Model):

    name = models.CharField(max_length=25, unique= True, blank= False)
    slug = models.SlugField(max_length=25, blank= True)

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name = self.name.title()
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class UserBlog(models.Model):
    author = models.ForeignKey(User,on_delete= models.CASCADE, related_name= 'user_blogs')
    headline = models.TextField(max_length=255, blank= False)
    category = models.ForeignKey(Category, default=6,on_delete= models.CASCADE, related_name= "user_blogs")
    body = models.TextField(max_length=4000, blank= False)
    source = models.URLField(blank=False, help_text= "Please provide a reputable source for reference")
    date_created = models.DateTimeField(auto_now_add= True)
    date_modified = models.DateTimeField(auto_now= True)
    alerts = models.BooleanField(default= True)
    bookmarkers = models.ManyToManyField(User, related_name= "bookmarks")

    class Meta:
        ordering = ('-date_created',)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete= models.DO_NOTHING, related_name= 'comments')
    date_created = models.DateTimeField(auto_now_add= True)
    body = models.TextField(max_length= 255, blank= False, help_text= "Enter Comment")
    blog = models.ForeignKey(UserBlog, on_delete= models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['-date_created',]

class Notifications(models.Model):
    owner = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'notifications')
    blog = models.ForeignKey(UserBlog, null= True, related_name= 'notifications', on_delete= models.CASCADE)
    label = models.CharField(max_length= 50)
    connected_account = models.ForeignKey(User, on_delete= models.CASCADE, blank= True, null= True, related_name= 'necessary_for_diversification')
    body = models.CharField(max_length= 150)
    viewed_status = models.IntegerField(default= 2)
    created_on = models.DateTimeField(auto_now_add= True, null= True)

    class Meta:
        ordering = ['-created_on',]