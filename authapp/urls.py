from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm

app_name = "authapp"

urlpatterns = [
    path('signup/', views.signupview, name= 'signup'),
    path('signup/<str:action>/otp-verify/', views.otp_verification_view, name= 'otp_verify'),
    path('welcome/', views.welcome_view, name= 'welcome'),
    path('login/', views.loginview, name= 'login'),
    path('user/<str:username>/', views.profile_view, name= 'profile'),
    path('user/follow/<str:username>/', views.follow_action_view, name= 'follow'),
    path('login/recover/', views.recovery_email_view, name= 'recovery_email'),
    path('login/recover/password/', views.password_recovery_view, name= 'password_recovery'),
    path('logout/', views.logoutview, name= 'logout'),
    path('account/settings/', views.settings_view, name= 'settings'),
    path('account/settings/general/', views.edit_profile, name= 'general_settings'),
    path('account/settings/login/', views.privacy_view, name= 'privacy_settings'),
    path('account/settings/login/password/', views.edit_password, name= 'password_settings'),
    path('account/settings/login/email/', views.edit_email, name= 'email_settings'),
    path('notifications/', views.notification_view, name= 'notifications'),
    path('network/<str:username>/<str:network_type>/', views.network_view, name= 'network'),

]