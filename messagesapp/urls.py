from django.urls import path
from .views import sendtextview, inboxview

app_name = 'messagesapp'

urlpatterns = [
    path("", inboxview, name= 'inbox'),
    path("send/<int:pk>/", sendtextview, name= 'send'),
]