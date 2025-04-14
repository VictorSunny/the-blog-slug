from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm, UserModel
from django import forms
from django.core.validators import RegexValidator
from django_countries.widgets import CountrySelectWidget

User = get_user_model()

username_format =  RegexValidator(
    regex= r"^\w+$",
    code= "invalid format",
    message= "username can only contain letters, numbers, and underscores",
)

name_format = RegexValidator(
    regex= r"^[A-Za-z]+$",
    code= "invalid format",
        message= "name can contain letters only",
)

form_css_styling = 'w-full h-full px-6 border border-black hover:border-white rounded-sm lg:rounded-lg bg-white'

class UserCreation(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'nationality', 'about']
        widgets = {'nationality': CountrySelectWidget(attrs= {'class': form_css_styling, 'required': True})}

    username = forms.CharField(widget= forms.TextInput(attrs={
        'placeholder': 'Username here please',
        'class': form_css_styling
        }), 
        validators= [username_format])

    first_name = forms.CharField(
            widget= forms.TextInput(
                attrs={
                    'placeholder': 'First name here please',
                    'class': form_css_styling
                }),
            validators= [name_format],
        )

    last_name = forms.CharField(
            widget= forms.TextInput(
                attrs={
                    'placeholder': 'Last name here please',
                    'class': form_css_styling
                }),
            validators= [name_format],
        )
    
    email = forms.EmailField(widget= forms.EmailInput(attrs={
        'placeholder': 'eMail here',
        'class': form_css_styling
    }))

    password1 = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder': 'Password here',
        'class': form_css_styling
    }))

    password2 = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder': 'Confirm password here',
        'class': form_css_styling
    }))

    about = forms.CharField(
        required= False,
        widget= forms.Textarea(attrs={
        'placeholder': 'Tell a little about yourself',
        'class': form_css_styling,
    }))


class UserUpdate(UserChangeForm):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    username = forms.CharField(
                widget= forms.TextInput(attrs={
                    'placeholder': 'Username here please',
                    'class': form_css_styling
                    }),
                validators= [username_format]
            )

    first_name = forms.CharField(
            widget= forms.TextInput(
                attrs={
                    'placeholder': 'First name here please',
                    'class': form_css_styling
                }),
            validators= [name_format],
        )

    last_name = forms.CharField(
            widget= forms.TextInput(
                attrs={
                    'placeholder': 'Last name here please',
                    'class': form_css_styling
                }),
            validators= [name_format],
        )

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget= forms.TextInput(attrs={
        'placeholder': 'email here',
        'class': form_css_styling
    }))
    password = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder': 'password here',
        'class': form_css_styling
    }))

    class Meta:
        model = User
        fields = ['email', 'password']
    

class PasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2',]

    old_password = forms.CharField(widget= forms.PasswordInput(attrs={
        'email': 'email here please',
        'class': form_css_styling
    }))
    new_password1 = forms.CharField(widget= forms.PasswordInput(attrs={
        'email': 'email here please',
        'class': form_css_styling
    }))
    new_password2 = forms.CharField(widget= forms.PasswordInput(attrs={
        'email': 'email here please',
        'class': form_css_styling
    }))

class EmailChange(UserChangeForm):
    confirm_password = forms.CharField(widget= forms.PasswordInput(attrs={
        'email': 'email here please',
        'class': form_css_styling
    }))

    email = forms.EmailField(widget= forms.EmailInput(attrs={
        'placeholder': 'eMail here',
        'class': form_css_styling
    }))

    class Meta:
        model = User
        fields = ['email', 'confirm_password']

class OTPForm(forms.Form):
    verification_code = forms.CharField(widget= forms.PasswordInput(attrs={
        'email': 'Enter OTP recieved in mail',
        'class': form_css_styling
    }))

class EmailForm(forms.Form):

    email = forms.EmailField(widget= forms.EmailInput(attrs={
        'placeholder': 'enter the email connected to your account',
        'class': form_css_styling
    }))

class PasswordRecoveryForm(forms.Form):
    new_password1 = forms.CharField(widget= forms.PasswordInput(attrs={
        'email': 'email here please',
        'class': form_css_styling
    }))
    new_password2 = forms.CharField(widget= forms.PasswordInput(attrs={
        'email': 'email here please',
        'class': form_css_styling
    }))