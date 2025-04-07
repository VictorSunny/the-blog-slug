from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import UserBlog, Comment
from decouple import config


standard_styling = 'w-full h-full p-2 lg:p-4 border border-black w-full hover:border-white rounded-sm lg:rounded-lg bg-white'


class BlogForm(forms.ModelForm):
    class Meta:
        model = UserBlog
        fields = ['headline', 'category', 'body', 'source']
        widgets = {
            'headline': forms.TextInput(attrs= {'class': standard_styling}),
            'category': forms.Select(attrs= {'class': standard_styling}),
            'body': forms.Textarea(attrs= {'class': standard_styling, 'minlength': config('MIN_ARTICLE_LENGTH')}),
            'source': forms.URLInput(attrs= {'class': standard_styling})
        }

       
class edit_blogForm(forms.ModelForm):
    class Meta:
        model = UserBlog
        fields = ['headline', 'body']
        widgets = {
            'headline': forms.TextInput(attrs= {'class': standard_styling}),
            'body': forms.Textarea(attrs= {'placeholder': 'write your article here', 'class': standard_styling}),
            }


    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body",]
        widgets = {
            'body': forms.Textarea(attrs= {'placeholder': 'write your comment here', 'class': standard_styling}),
            }

