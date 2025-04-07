from django.urls import path
from .views import send_text_view, inbox_view, archive_chat_view

app_name = 'messagesapp'

urlpatterns = [
    path('<inbox_type>/', inbox_view, name= 'inbox'),
    path('chat/<str:username>/', send_text_view, name= 'send'),
    path('close/<int:id>/', archive_chat_view, name= 'archive')
]