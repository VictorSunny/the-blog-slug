from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
import json
from ..models import OTPVerification
from core.models import Notifications

User = get_user_model()
#Tests for authapp's views.py file


class AuthappViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
            create test user to be used throughout test class
        """
        
        cls.testuser = User.objects.create_user(
                username= "testuser1",
                email= "test1@user.com",
                first_name= "first",
                last_name= "user",
                password= "AA@@bb11",
                nationality= "NG",
            )
        
        cls.testuser3 = User.objects.create_user(
                username= "testuser3",
                email= "test3@user.com",
                first_name= "third",
                last_name= "user",
                password= "AA@@bb33",
                nationality= "NG",
            )
        
    def login_first_user(self):
        self.client.login(username= "test1@user.com", password= "AA@@bb11")

        


    
    def test_sequence_signup_otp_login_welcome(self):
        """
            test successful sequence from user signup to otp verification,
            from otp verification to login,
            finally, from login to welcome page. New users must see welcome page for proper introduction 
        """

        #check for correct template use
        signup_page = self.client.get(reverse("authapp:signup"))
        self.assertTemplateUsed(signup_page, "signup.html")
        self.assertEqual(signup_page.status_code, 200)

        #send post request with user details for signup
        signup_post_action = self.client.post(
            reverse("authapp:signup"),
            {
                "username": "testuser2",
                "email": "test2@user.com",
                "first_name": "second",
                "last_name": "user",
                "password1": "AA@@bb22",
                "password2": "AA@@bb22",
                "nationality": "NG",
            },
        )
        print(signup_post_action.content)
        #url for otp redirection after signup
        otp_signup_auth_url = reverse("authapp:otp_verify", kwargs={"action": "signup"})
        #check if successful signup redirects to signup otp page
        self.assertRedirects(signup_post_action, otp_signup_auth_url)

        #get signup otp page to trigger otp generation
        otp_query_page = self.client.get(otp_signup_auth_url)
        self.assertTemplateUsed(otp_query_page, "otp_verify.html")
        #retrieve otp generated
        new_user_otp = OTPVerification.objects.get(email= "test2@user.com").code

        #post generated otp to complete signup process
        otp_success_response = self.client.post(otp_signup_auth_url, {"verification_code": new_user_otp})

        #check if successful submission redirects to login page
        self.assertRedirects(otp_success_response, reverse("authapp:login"))

        #login with valid credentials
        login_success_response = self.client.post(reverse("authapp:login"), {"username": "test2@user.com", "password": "AA@@bb22"})
        #check if successful login redirects to welcome page
        self.assertRedirects(login_success_response, reverse("authapp:welcome"))

    def test_should_login_and_redirect_to_homepage(self):
        """
         tests login for regular users works and redirects to homepage
        """

        template = self.client.get(reverse('authapp:login'))
        self.assertTemplateUsed(template, "login.html")

        login_success_response = self.client.post(reverse("authapp:login"), {"username": "test1@user.com", "password": "AA@@bb11"})
        self.assertRedirects(login_success_response, reverse("core:home"))

    def test_profile_page(self):
        """
            tests profile page is properly rendered with needed data
        """
        profile_page = self.client.get(reverse("authapp:profile", kwargs={"username": "testuser1"}))
        self.assertTemplateUsed(profile_page, "profile.html")
        
        #check that the profile view is loaded with the needed context data
        expected_context_data = ["slug", "all_blogs"]
        for context in expected_context_data:
            self.assertIn(context, profile_page.context)
    
    def test_settings_view(self):
        """
            test for proper rendering of settings page
        """

        #login first as view is login protected
        self.login_first_user()

        settings_page = self.client.get(reverse("authapp:settings"))
        
        self.assertTemplateUsed(settings_page, "settings.html")

    def test_privacy_settings_view(self):
        """
            test for proper rendering of privacy settings page
        """

        #login first as view is login protected
        self.login_first_user()

        privacy_settings_page = self.client.get(reverse("authapp:privacy_settings"))
        self.assertTemplateUsed(privacy_settings_page, "privacy_settings.html")

    def test_user_update_view(self):
        """
            test for proper update of user details
        """
        self.login_first_user()

        #retrieve user object for update
        test_user = User.objects.get(email= "test1@user.com")
        
        #set variables for user details before change
        initial_username = test_user.username
        initial_first_name = test_user.first_name
        initial_last_name = test_user.last_name
        
        #check that general settings page uses the right template
        general_settings_page = self.client.get(reverse("authapp:general_settings"))
        self.assertTemplateUsed(general_settings_page, "edit_profile.html")

        #send post request for user details update
        successful_update_response = self.client.post(
            reverse("authapp:general_settings"),
            {
                "username": "changed_username",
                "first_name": "changedfirstname",
                "last_name": "changedlastname"
            }
        )

        #retrieve user object again to reflect changes
        test_user = User.objects.get(email= "test1@user.com")

        #set variables for updated user details
        changed_username = test_user.username
        changed_first_name = test_user.first_name
        changed_last_name = test_user.last_name

        #check that all changes took effect in the database
        self.assertNotEqual(initial_username, changed_username)
        self.assertNotEqual(initial_first_name, changed_first_name)
        self.assertNotEqual(initial_last_name, changed_last_name)

        #check that user is redirected to profile page upon successful update operation
        self.assertRedirects(successful_update_response, reverse("authapp:profile", kwargs={"username": changed_username}))
        
    
    def test_email_update(self):

        self.login_first_user()

        email_change_page = self.client.get(reverse("authapp:email_settings"))
        self.assertTemplateUsed(email_change_page, "edit_email.html")

        #retrieve user object for update
        test_user = User.objects.get(email= "test1@user.com")
        
        #set variables for user details before change
        initial_email = test_user.email
        new_email = "changed@email.com"

        #send post request for user details update
        successful_update_response = self.client.post(
            reverse("authapp:email_settings"),
            {
                "email": new_email,
                "confirm_password": "AA@@bb11"
            }
        )

        #url for otp redirection after update
        otp_email_auth_url = reverse("authapp:otp_verify", kwargs={"action": "update_email"})
        #check that user is redirected to profile page upon successful update operation
        self.assertRedirects(successful_update_response, otp_email_auth_url)
        
        #get signup otp page to trigger otp generation
        otp_query_page = self.client.get(otp_email_auth_url)
        self.assertTemplateUsed(otp_query_page, "otp_verify.html")
        #retrieve otp generated
        new_user_otp = OTPVerification.objects.get(email= new_email).code

        #post generated otp to complete email change process
        otp_success_response = self.client.post(otp_email_auth_url, {"verification_code": new_user_otp})

        #check if successful submission redirects to login page
        self.assertRedirects(otp_success_response, reverse("authapp:login"))

        #reset email in database for other tests to carry out as normal
        test_user.email = "test1@user.com"
        test_user.save()

    def test_password_update(self):

        self.login_first_user()

        email_change_page = self.client.get(reverse("authapp:password_settings"))
        self.assertTemplateUsed(email_change_page, "edit_password.html")

        #retrieve user object for update
        test_user = User.objects.get(email= "test1@user.com")
        
        #set variables for user details before change
        initial_password = "AA@@bb11"
        new_password = "BB@@aa99"

        self.assertTrue(test_user.check_password(initial_password))

        #send post request for user details update
        successful_update_response = self.client.post(
            reverse("authapp:password_settings"),
            {
                "old_password": initial_password,
                "new_password1": new_password,
                "new_password2": new_password
            }
        )

        #url for otp redirection after update
        otp_password_auth_url = reverse("authapp:otp_verify", kwargs={"action": "update_password"})
        #check that user is redirected to profile page upon successful update operation
        self.assertRedirects(successful_update_response, otp_password_auth_url)

        #get signup otp page to trigger otp generation
        otp_query_page = self.client.get(otp_password_auth_url)
        self.assertTemplateUsed(otp_query_page, "otp_verify.html")
        #retrieve otp generated
        new_user_otp = OTPVerification.objects.get(email= "test1@user.com").code

        #post generated otp to complete password update process
        otp_success_response = self.client.post(otp_password_auth_url, {"verification_code": new_user_otp})

        #check if successful submission redirects to login page
        self.assertRedirects(otp_success_response, reverse("authapp:login"))

        #check if user password has been changed
        test_user = User.objects.get(email= "test1@user.com")
        self.assertTrue(test_user.check_password(new_password))
        self.assertFalse(test_user.check_password(initial_password))

        #reset password for other tests to run as normal
        test_user.set_password("AA@@bb11")
        test_user.save()


    def test_password_recovery(self):

        self.login_first_user()

        email_change_page = self.client.get(reverse("authapp:recovery_email"))
        self.assertTemplateUsed(email_change_page, "recovery_email.html")

        #retrieve user object for update
        test_user = User.objects.get(email= "test1@user.com")

        #set variables for user details before change
        initial_password = "AA@@bb11"
        new_password = "BB@@aa99"

        #confirm initial password is correct
        self.assertTrue(test_user.check_password(initial_password))

        #send post request with user email connected to account to recieve OTP
        successful_email_post_response = self.client.post(
            reverse("authapp:recovery_email"),
            {
                "email": test_user.email
            }
        )

        #url for otp redirection after update
        otp_password_recovery_url = reverse("authapp:otp_verify", kwargs={"action": "password_recovery"})

        #check that user is redirected to profile page upon successful update operation
        self.assertRedirects(successful_email_post_response, otp_password_recovery_url)

        #get signup otp page to trigger otp generation
        otp_query_page = self.client.get(otp_password_recovery_url)
        self.assertTemplateUsed(otp_query_page, "otp_verify.html")
        #retrieve otp generated
        new_user_otp = OTPVerification.objects.get(email= test_user.email).code

        #post generated otp to complete password update process
        otp_success_response = self.client.post(otp_password_recovery_url, {"verification_code": new_user_otp})

        #check if successful submission redirects to login page
        self.assertRedirects(otp_success_response, reverse("authapp:password_recovery"))

        #get password recovery page
        password_recovery_page = self.client.get(reverse("authapp:password_recovery"))
        self.assertTemplateUsed(password_recovery_page, "password_recovery.html")

        successful_password_recovery_response = self.client.post(
            reverse("authapp:password_recovery"),
            {
                "new_password1": new_password,
                "new_password2": new_password,
            }
        )

        self.assertRedirects(successful_password_recovery_response, reverse("authapp:login"))

        #check if user password has been changed
        test_user = User.objects.get(email= "test1@user.com")
        self.assertTrue(test_user.check_password(new_password))
        self.assertFalse(test_user.check_password(initial_password))
        
        #reset password for other tests to run as normal
        test_user.set_password("AA@@bb11")
        test_user.save()

    
    def test_user_following(self):

        self.login_first_user()

        celebrity = User.objects.get(email= "test3@user.com")
        follower = User.objects.get(email= "test1@user.com")

        #get url to follow celebrity
        celebrity_network_url = reverse("authapp:follow", kwargs={"username": celebrity.username})

        #visit follow_action_view endpoint to trigger follow action
        self.client.get(celebrity_network_url)

        #check celebrity is followed by follower
        self.assertTrue( celebrity in follower.following.all())
        self.assertTrue( follower in celebrity.followers.all())

        #check that the celebrity recieved a notification on their new follower
        Notifications.objects.filter(owner= celebrity).get(label= "new follower")
        
        #visit follow_action_view endpoint again to trigger unfollow action
        self.client.get(celebrity_network_url)

        #check celebrity is followed by follower
        self.assertFalse( celebrity in follower.following.all())
        self.assertFalse( follower in celebrity.followers.all())

        #check that a user cannot follow themself
        unsuccessful_follow_response = self.client.get(reverse("authapp:follow", kwargs={"username": follower.username}))
        self.assertTrue(unsuccessful_follow_response.status_code == 403)


    def test_notifications_view(self):

        self.login_first_user()

        notification_page = self.client.get(reverse("authapp:notifications"))
        self.assertTemplateUsed(notification_page, "notifications.html")

        self.assertIn("notifications", notification_page.context)
        
    def test_network_view(self):

        self.login_first_user()

        expected_context_data = ["data", "total_pages", "network_type", "page_owner"]
        network_types = ["followers", "following"]

        for type in network_types:
            network_page_url = reverse(
                "authapp:network",
                kwargs= {
                    "username": "testuser1",
                    "network_type": type
                }
            )

            network_page = self.client.get(network_page_url)
            self.assertTemplateUsed(network_page, "network.html")

            for context in expected_context_data:
                self.assertIn(context, network_page.context)       
        
        