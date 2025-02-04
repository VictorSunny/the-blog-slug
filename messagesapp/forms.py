from django import forms
from .models import Conversation, SlugMessages

standard_styling = 'w-full text-lg p-4 px-4 h-30 text-white'
class ChatForm(forms.ModelForm):
    class Meta:
        model = SlugMessages
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'enter message' ,'class': standard_styling})
        }