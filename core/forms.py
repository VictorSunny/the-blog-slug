from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import UserBlog, Comment

class UserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'groups']

    username = forms.CharField(widget= forms.TextInput(attrs={
        'placeholder': 'Username here please',
        'class': 'w-full h-full px-6 rounded-xl  bg-white'
    }))
    first_name = forms.CharField(widget= forms.TextInput(attrs={
        'placeholder': 'First name here please',
        'class': 'w-full h-full px-6 rounded-xl  bg-white'
    }))
    last_name = forms.CharField(widget= forms.TextInput(attrs={
        'placeholder': 'Last name here please',
        'class': 'w-full h-full px-6 rounded-xl  bg-white'
    }))
    email = forms.CharField(widget= forms.EmailInput(attrs={
        'placeholder': 'eMail here',
        'class': 'w-full h-full px-6 rounded-xl bg-white'
    }))
    password1 = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder': 'Password here',
        'class': 'w-full h-full px-6 rounded-xl bg-white'
    }))
    password2 = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder': 'Confirm password here',
        'class': 'w-full h-full px-6 rounded-xl bg-white'
    }))

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget= forms.TextInput(attrs={
        'placeholder': 'username here please',
        'class': 'w-full h-full px-6 rounded-xl bg-white'
    }))
    password = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder': 'password here',
        'class': 'w-full h-full px-6 rounded-xl bg-white'
    }))


standard_styling = 'w-full h-full ml-4 mr-2 mt-2 mb-2 rounded-xl text-l  bg-white'
class BlogForm(forms.ModelForm):
    class Meta:
        model = UserBlog
        fields = ['headline', 'category', 'body', 'source']
        widgets = {
            'category': forms.Select(attrs= {'class': standard_styling}),
            'body': forms.Textarea(attrs= {'placeholder': 'write your article here', 'class': standard_styling}),
            'healine': forms.Textarea(attrs= {'helptext': 'enter a striking headline', 'class': standard_styling}),
            'source': forms.URLInput(attrs= {'helptext': 'enter a reputable source', 'class': 'w-full h-20 rounded-xl'})
            }
        
class BlogEditForm(forms.ModelForm):
    class Meta:
        model = UserBlog
        fields = ['headline', 'body']
        widgets = {
            'body': forms.Textarea(attrs= {'placeholder': 'write your article here', 'class': standard_styling}),
            'healine': forms.Textarea(attrs= {'helptext': 'enter a striking headline', 'class': standard_styling}),
            }


    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body",]
        widgets = {
            'body': forms.Textarea(attrs= {'placeholder': 'write your comment here', 'class': 'w-full p-2 bg-white'}),
            }

