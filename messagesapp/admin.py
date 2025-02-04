from django.contrib import admin
from .models import Conversation, SlugMessages
# Register your models here.

admin.site.register(Conversation)
admin.site.register(SlugMessages)