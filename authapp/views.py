from django.shortcuts import render, redirect
from .forms import UserCreation, LoginForm, UserUpdate, PasswordForm, EmailChange, OTPForm, EmailForm, PasswordRecoveryForm
from django.contrib.auth import logout, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.views import View
import secrets
from .models import OTPVerification
from django.core.mail import send_mail
from django.urls import reverse
from decouple import config
from datetime import timedelta
from django.utils import timezone
from core.models import Notifications
from decouple import config
from core.custom_functions import notification_cleanser

# Create your views here.

#Import custom authentication user model and assign to variable 'User'
User = get_user_model()


#user singup view
def signupview(request):
    if request.method == 'POST':
        form = UserCreation(request.POST)
        if form.is_valid():
            user_data= form.cleaned_data

            #create session data with account details for account creation after otp verification
            request.session['data'] = dict(user_data)

            #redirect to otp verification page with signup data
            return redirect('authapp:otp_verify', 'signup')
    else:
        form = UserCreation()
    return render(request, "signup.html", {"form": form}, status= 200)


#user login view
def loginview(request):
    if request.method == 'POST':
        request.POST._mutable = True
        request.POST['username']= request.POST['username'].lower()
        request.POST._mutable = False
        form = LoginForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            try:
                if request.session['new']:
                    #if user is new, redirect user to the welcome page
                    #delete session data signifying that the user is new
                    del request.session['new']
                    return redirect('authapp:welcome')
            except:
                return redirect('core:home')

    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

def profile_view(request, username):
    slug = User.objects.get(username= username)
    user_blogs = slug.user_blogs.all()
    page = request.GET.get('p')

    paginator_class = Paginator(user_blogs, 8)
    user_blogs = paginator_class.get_page(page)

    return render(request, 'profile.html', {'slug': slug, 'all_blogs': user_blogs})


#view for seeing user followers and following
@login_required()
def network_view(request, username, network_type):
    page_owner = User.objects.get(username= username)
    page = request.GET.get('page')

    followers = page_owner.followers.all()
    following = page_owner.following.all()
    
    network = {"following": following, "followers": followers}

    #access 'network' dictionary based on 'network_type' entered
    paginator = Paginator(network[network_type], 10)
    data = paginator.get_page(page)

    return render(request, 'network.html', {
        'data': data,
        'total_pages': paginator.num_pages,
        'network_type': network_type,
        'page_owner': page_owner.username
        })


#otp verification view for signup and account security updates
def otp_verification_view(request, action):

    #retrieve session data with user information for otp verification against matching user account
    user_data = request.session.get('data')
    if action == 'signup':

        #extract verified password from signup page to set user password
        user_data['password'] = user_data['password1']

        #delete unsupported fields from signup json of session data to allow usage for user model object creation
        del user_data['password1']
        del user_data['password2']
        mail_subject = 'A WORM WELCOME'

    elif action == 'update_password':

        #set session data for new password to be used for user object update
        new_password = user_data['new_password2']
        user_data['email'] = request.user.email
        mail_subject = 'WORM PASSWORD CHANGE'

    elif action == 'update_email':

        #set session data for new email to be used for user email update
        new_email = user_data['email']  
        mail_subject = 'WORM EMAIL CHANGE'

    elif action == 'password_recovery':
        mail_subject = 'ACCOUNT RECOVERY'

    try:

        #retrieve otp object if exists
        verification_object = OTPVerification.objects.get(email= user_data['email'])

        #delete otp object if expired
        if timezone.now() > verification_object.created_at + timedelta(minutes=3):
            verification_object.delete()
            print('expired otp deleted')
            return redirect(request.path)
        else:
            otp = verification_object.code
            print(otp)
            print('retrieved locally')
    except:

        #create otp object if expired & deleted or does not exist
        otp = secrets.token_hex(5)
        print(otp)

        #send otp to user email if in production
        #view output console in development to see otp
        if config('DEBUG', cast= bool) == False:
            verification_email = send_mail(
                subject= mail_subject,
                message= f'Your signup OTP code: {otp}',
                recipient_list= [user_data['email'],],
                from_email= config('DEFAULT_FROM_EMAIL'),
            )

        #save otp as an object to be retrieved and reused within allowed window
        OTPVerification.objects.create(
            email= user_data['email'],
            code= otp,
        )

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['verification_code'] == otp:

                if action == 'signup':
                    new_user = User.objects.create_user(**user_data)
                    for field in user_data:
                        if field != 'email':
                            new_user.field = user_data[field]
                    new_user.save()

                    #create signifier that account is new. new account gets redirected to welcome page upon login
                    request.session['new'] = ['new']

                elif action == 'update_password':
                    user = User.objects.get(id= request.user.id)
                    password = user.set_password(new_password)
                    user.save()

                elif action == 'update_email':
                    user = User.objects.get(id= request.user.id)
                    user.email = new_email
                    user.save()

                if action == 'password_recovery':

                    #create session email data to allow otp view to access the email for otp verification
                    request.session['email'] = request.session['data']['email']
                    return redirect('authapp:password_recovery')
                
                #delete session data
                del request.session['data']
                return redirect('authapp:login')
            else:
                form.add_error(field= 'verification_code', error= 'Invalid code. Please try again')
    else:
        form = OTPForm()
    return render(request, 'otp_verify.html', {'form': form})
    


#logout view
login_required()    
def logoutview(request):
    logout(request)
    return redirect("core:home")

#account settings view
@login_required()
def settings_view(request):
    return render(request, 'settings.html')

#view for editing basic user profile details
@login_required()
def edit_profile(request):
    form = UserUpdate(
            instance= request.user
        )
    if request.method == 'POST':
        form = UserUpdate(data= request.POST, instance= request.user)
        if form.is_valid():
            user = form.save()
            user.save()
            profile_url = reverse('authapp:profile', kwargs={"username": user.username})
            return redirect(profile_url)
        
    return render(request, "edit_profile.html", {"form": form})

@login_required()
def privacy_view(request):
    return render(request, 'privacy_settings.html')

#view for editing user password
@login_required()
def edit_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            request.session['data'] = dict(form.cleaned_data)
            return redirect('authapp:otp_verify', 'update_password')
    else:
        form = PasswordForm(request.user)
        
    return render(request, "edit_password.html", {"form": form})

#view for editing user email
@login_required()
def edit_email(request):
    user_object = User.objects.get(id= request.user.id)
    if request.method == 'POST':
        form = EmailChange(data= request.POST, instance= request.user)
        if form.is_valid():

            #extract password entered into form to check against current user password 
            password_entered = form.cleaned_data['confirm_password']
            if user_object.check_password(password_entered):

                #alter session data to contain new user email entered 
                request.session['data'] = dict(form.cleaned_data)

                return redirect('authapp:otp_verify', 'update_email')
            
            else:

                #if form is password entered is incorrect, raise an error
                form.add_error('confirm_password', 'Incorrect password. Please try again.')

    else:
        form = EmailChange(
            instance= request.user
        )
        
    return render(request, "edit_email.html", {"form": form})

 

#account recovery view for taking and verifying user email inputs for otp verification
def recovery_email_view(request):
    user_emails = User.objects.all().values('email')
    emails = []
    #create dictionary of existing email addresses in database
    for email in user_emails:
        emails.append(email['email'])
    
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email_entered = form.cleaned_data['email']

            #check if email entered by user is connected to any existing account for recovery
            if email_entered in emails:

                #set session data with user information to be used for user validation in otp verification page
                request.session['data'] = dict(form.cleaned_data)

                return redirect('authapp:otp_verify', 'password_recovery')
            
            else:
                form.add_error('email', 'Rejected. This email is not connected to any account.')

    else:
        form = EmailForm()
        
    return render(request, "recovery_email.html", {"form": form})

#account recovery view for setting new user password upon successful otp verification using account email
def password_recovery_view(request):
    
    if request.method == 'POST':
        form = PasswordRecoveryForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['new_password2'] == form.cleaned_data['new_password1']:
                recovered_user = User.objects.get(email= request.session['email'])
                recovered_user.set_password(form.cleaned_data['new_password1'])
                recovered_user.save()

                #after confirming password, delete session data containing user email
                del request.session['email']
                #redirect to login page upon successful account update
                return redirect('authapp:login')
            else:
                 form.add_error(field= 'new_password2', error= 'Passwords do not match')
    
    else:
        form = PasswordRecoveryForm()

    return render(request, 'password_recovery.html', {'form': form})

#view for following user
@login_required()
def follow_action_view(request, username):
    prev_page = request.META.get("HTTP_REFERER", "/")

    visitor = request.user
    profile_owner = get_object_or_404(User, username= username)

    if profile_owner in visitor.following.all():
        print('unfollowed')
        visitor.following.remove(profile_owner)
        profile_owner.followers.remove(visitor)
    else:
        print('followed')
        if visitor != profile_owner:
            visitor.following.add(profile_owner)
            profile_owner.followers.add(visitor)
            
            unparsed_body= f"{visitor.username} just followed you. keep posting! ;)"
            body = notification_cleanser(profile_owner.id, unparsed_body)

            #send notification to followed user
            alert = Notifications.objects.create(
                owner= profile_owner,
                label= f"new follower",
                body= body,
                connected_account= visitor
            )
            alert.save()
        else:
            return HttpResponseForbidden({"message": "request forbidden. you cannot follow yourself"})

    return redirect(prev_page)

#view for retrieving all notifications from database based on visitor, and rendering
@login_required()
def notification_view(request):
    page = request.GET.get("p")

    try:
        notifications = request.user.notifications.all() 
        for alert in notifications:
            print(alert)
            if alert.viewed_status > 0:
                alert.viewed_status -= 1
                alert.save()
        
        paginator_class = Paginator(notifications, 8)
        notifications = paginator_class.get_page(page)

    except:
        notifications = None

    return render(request, "notifications.html", {"notifications": notifications,})

#welcome view for new users       
def welcome_view(request):
    return render(request, 'welcome.html')