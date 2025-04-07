from django import forms
from .models import Conversation, SlugMessages

standard_styling = 'w-full lg:h-20 h-10 p-2 border border-black w-full hover:border-white rounded-sm lg:rounded-lg bg-white'
class ChatForm(forms.ModelForm):
    class Meta:
        model = SlugMessages
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'enter message' ,'class': standard_styling})
        }