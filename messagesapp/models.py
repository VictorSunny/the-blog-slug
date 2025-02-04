from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Conversation(models.Model):
    slugs = models.ManyToManyField(User, related_name= "conversations")
    date_created = models.DateTimeField(auto_now_add= True)
    date_modified = models.DateTimeField(auto_now= True)

    class Meta:
        ordering = ['-date_modified',]
    


class SlugMessages(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete= models.CASCADE, related_name= "messages")
    text = models.TextField(max_length=500)
    sender = models.ForeignKey(User, on_delete= models.DO_NOTHING, related_name= "sent_messages")
    time_sent= models.DateTimeField(auto_now_add= True)
    
    class Meta:
        ordering = ['time_sent',]