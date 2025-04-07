from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import UserBlog, Category, Comment, Notifications
from django.db.models import Q



User = get_user_model()

#Tests for core app's views.py

class ViewTest(TestCase):

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
                password= "AA@@bb11"
            )
        
        cls.testuser3 = User.objects.create_user(
                username= "testuser3",
                email= "test3@user.com",
                first_name= "third",
                last_name= "user",
                password= "AA@@bb33"
            )
        
        Category.objects.create(name= "test_category").save()


        
    def login_first_user(self):
        self.client.login(username= "test1@user.com", password= "AA@@bb11")
    

    def test_home_view(self):
        """
            test for home page
        """
        homepage = self.client.get(reverse("core:home"))
        self.assertTemplateUsed(homepage, "index.html")
        self.assertIn("article_dict", homepage.context)

    def test_all_blogs_view(self):
        """
            test for all_blogs_view responsible for rendering all blogs posted by users with pagination and filter support
        """
        all_blogs_url = reverse("core:all_blogs")

        all_blogs_page = self.client.get(all_blogs_url)
        self.assertTemplateUsed(all_blogs_page, "all_blogs.html")

        # check that blog page is loaded with necessary context data
        expected_context_data = [
            "all_blogs",
            "categories",
            "category_filter",
            "page_title"
        ]

        for context in expected_context_data:
            self.assertTrue(context in all_blogs_page.context)

 
 
    def test_bookmarked_blogs_view(self):
        """
            test for all_blogs_view responsible for rendering blogs bookmarked by the logged in user
        """
        self.login_first_user()

        bookmarked_blogs_url = reverse("core:bookmarked_blogs")

        bookmarked_blogs_page = self.client.get(bookmarked_blogs_url)
        self.assertTemplateUsed(bookmarked_blogs_page, "all_blogs.html")

        # check that blog page is loaded with necessary context data
        expected_context_data = [
            "all_blogs",
            "categories",
            "page_title"
        ]

        for context in expected_context_data:
            self.assertTrue(context in bookmarked_blogs_page.context)



    def test_sequence_blog_posting_viewing_commenting_notifications_updating_bookmarking(self):
        """
            test for blog posting action
        """
        
        ########################################################################################
            # TEST FOR BLOG POSTING
        ########################################################################################

        #login user and assign to variable "test_user" for testings ahead
        self.login_first_user()
        test_user = User.objects.get(username= "testuser1")

        test_reader = User.objects.get(username= "testuser3")

        blog_form_url = reverse("core:create_blog")
        blog_form_page = self.client.get(blog_form_url)

        self.assertTemplateUsed(blog_form_page, "create_blog.html")
        # check that form is passed on to create_blog_view
        self.assertTrue("form" in blog_form_page.context)

        # assign original values to variables for comparisons later
        initial_blog_body = "set your desired character length as your MIN_ARTICLE_LENGTH in your .env file. advisable to use a value < 30 for testing"
        initial_blog_headline = "django user tests app"

        successful_blog_post_response = self.client.post(
            blog_form_url,
            {
                "headline": initial_blog_headline,
                "category": 1,
                "source": "https://www.trustmebro.com",
                "body": initial_blog_body,
            },
        )
        self.assertTrue(successful_blog_post_response.status_code == 302)
        
        test_blog = UserBlog.objects.get(body= initial_blog_body)
        test_blog_url = reverse("core:blog", kwargs={"pk": test_blog.id})


        ########################################################################################
            # TEST FOR BLOG VIEWING AFTER SUCCESSFUL POSTING
        ########################################################################################

        test_blog_page = self.client.get(test_blog_url)
        self.assertTemplateUsed(test_blog_page, "blog_page.html")

        # check that user is redirected to blog page after successful blog posting
        self.assertRedirects(successful_blog_post_response, test_blog_url)

        # check that blog page is loaded with necessary context data
        expected_context_data = ["blog", "form", "comments"]

        for context in expected_context_data:
            self.assertIn(context, test_blog_page.context)


        ########################################################################################
            # TEST FOR BLOG COMMENTING
        ########################################################################################
        
        blog_author_comment = "i am commenting on my own blog, so this shouldn't trigger a notification to be sent to me"
        successful_comment_post_response = self.client.post(
            test_blog_url,
            {
                "body": blog_author_comment
            }
        )

        #check that comment has been successfully posted under blog
        test_blog = UserBlog.objects.get(body= initial_blog_body)
        self.assertTrue(test_blog.comments.filter(body= blog_author_comment).exists() )
        self.assertRedirects(successful_comment_post_response, test_blog_url)


        # blog notifications are on by default, however blog author should not recieve a notification for the new comment
        # as the new comment is posted by logged in user and the blog owner: testuser
        
        # check that no new notification has been logged in user is the author of the test blog

        self.assertFalse( Notifications.objects.filter(body= blog_author_comment).exists() )

        ##############  LOGIN IN WITH A DIFFERENT USER: TEST_READER
        ##############  THIS USER IS NOT THE BLOG AUTHOR
        ##############  A COMMENT POST FROM THIS TEST_READER ACCOUNT SHOULD TRIGGER A NOTIFICATION TO BE SENT TO THE BLOG AUTHOR

        self.client.logout()
            
        self.client.login(username= "test3@user.com", password= "AA@@bb33")

        test_reader_comment_1 = "i don't own this blog, so this comment should trigger a notification for the blog author"
        successful_comment_post_response_1 = self.client.post(
            test_blog_url,
            {
                "body": test_reader_comment_1
            }
        )


        #check that comment has been successfully posted under blog
        test_blog = UserBlog.objects.get(body= initial_blog_body)


        self.assertTrue(test_blog.comments.filter(body= test_reader_comment_1).exists() )
        self.assertRedirects(successful_comment_post_response_1, test_blog_url)

        # blog notifications are on by default, so check that blog author recieved a notification for the new comment
        
        ### check that a new notification has been created for test_reader's comment on test_user's blog

        self.assertTrue( Notifications.objects.filter(Q(owner= test_user) & Q(connected_account= test_reader) ).exists() )

        # clear newly created notification for further testings

        Notifications.objects.all().delete()
        self.assertTrue( len(Notifications.objects.all()) == 0 )

        ##############  LOGOUT TEST_READER ACCOUNT
        ##############  LOGIN IN BACK WITH BLOG_AUTHOR ACCOUNT TO CARRY OUT OTHER TESTS

        self.client.logout()
        self.login_first_user()

        ########################################################################################
            # TEST FOR BLOG NOTIFICATIONS ENABLE/DISABLE
        ########################################################################################
        
        blog_notification_toggle_url = reverse("core:blog_alerts", kwargs={"blog_id": test_blog.id})

        # visit blog_alert_view endpoint to turn blog notifications from default "on" to "off"
        self.client.get(blog_notification_toggle_url)

        ##############  LOGIN IN WITH A DIFFERENT USER: TEST_READER
        ##############  THIS USER IS NOT THE BLOG AUTHOR
        ##############  A COMMENT POST FROM THIS TEST_READER ACCOUNT SHOULD TRIGGER A NOTIFICATION TO BE SENT TO THE BLOG AUTHOR
        ##############  HOWEVER NOTIFICATION WILL NOT BE CREATED AS BLOG NOTIFICATIONS HAVE BEEN TURNED OFF BY THE AUTHOR

        self.client.logout()
            
        self.client.login(username= "test3@user.com", password= "AA@@bb33")

        # initiate comment posting

        test_reader_comment_2 = "notifcations have been turned off by the blog author: test user, so this should not create a new notification"
        successful_comment_post_response_2 = self.client.post(
            test_blog_url,
            {
                "body": test_reader_comment_2
            }
        )

        #check that comment has been successfully posted under blog
        test_blog = UserBlog.objects.get(body= initial_blog_body)
        self.assertTrue(test_blog.comments.filter(body= test_reader_comment_2).exists() )
        self.assertRedirects(successful_comment_post_response_2, test_blog_url)

        # blog notifications are on by default, so check that blog author recieved a notification for the new comment
        
        ### check that no notification has been created for test_reader's comment on test_user's blog

        self.assertFalse( Notifications.objects.filter(Q(owner= test_user) & Q(connected_account= test_reader) ).exists() )

        ##############  LOGOUT TEST_READER ACCOUNT
        ##############  LOGIN IN BACK WITH BLOG_AUTHOR ACCOUNT TO TURN BLOG NOTIFICATIONS BACK ON

        self.client.logout()
        self.login_first_user()

        # visit blog_alert_view endpoint to turn blog notifications back on
        self.client.get(blog_notification_toggle_url)

        ##############  LOGIN IN WITH A DIFFERENT USER: TEST_READER
        ##############  THIS USER IS NOT THE BLOG AUTHOR
        ##############  A COMMENT POST FROM THIS TEST_READER ACCOUNT SHOULD TRIGGER A NOTIFICATION TO BE SENT TO THE BLOG AUTHOR

        self.client.logout()
            
        self.client.login(username= "test3@user.com", password= "AA@@bb33")

        # initiate comment posting

        test_reader_comment_3 = "notifcations have been turned back on by the test user, so this should trigger a new notification"
        successful_comment_post_response_3 = self.client.post(
            test_blog_url,
            {
                "body": test_reader_comment_3
            }
        )

        #check that comment has been successfully posted under blog
        test_blog = UserBlog.objects.get(body= initial_blog_body)
        self.assertTrue(test_blog.comments.filter(body= test_reader_comment_3).exists() )
        self.assertRedirects(successful_comment_post_response_3, test_blog_url)

        test_reader_comment_4 = "notifcations have been turned back on by the test user, so again, this should trigger a new notification"
        successful_comment_post_response_4 = self.client.post(
            test_blog_url,
            {
                "body": test_reader_comment_4
            }
        )

        #check that comment has been successfully posted under blog
        test_blog = UserBlog.objects.get(body= initial_blog_body)
        self.assertTrue(test_blog.comments.filter(body= test_reader_comment_4).exists() )
        self.assertRedirects(successful_comment_post_response_4, test_blog_url)

        ### check that notifications have been created for test_reader's comments on test_user's blog

        self.assertTrue( Notifications.objects.filter(Q(owner= test_user) & Q(connected_account= test_reader) ).exists() )

        # test_reader account has added 3 comments to the test blog so far
        # confirm that there is no duplication of notifications for this repeated action
        # notification cleaning should be enforced in blog_view using the notification_cleanser function

        self.assertTrue( len(Notifications.objects.filter(Q(owner= test_user) & Q(connected_account= test_reader))) == 1 )

        ##############  LOGOUT TEST_READER ACCOUNT
        ##############  LOGIN IN BACK WITH BLOG_AUTHOR ACCOUNT TO CARRY OUT OTHER TESTS

        self.client.logout()
        self.login_first_user()        
        

        ########################################################################################
            # TEST FOR BLOG UPDATING
        ########################################################################################

        blog_update_url = reverse("core:edit_blog", kwargs={"pk": test_blog.id})

        # check that page is rendered properly
        blog_update_page = self.client.get(blog_update_url)
        self.assertTemplateUsed(blog_update_page, "edit_blog.html")

        # check that form is passed on to edit_blog_view
        self.assertTrue("form" in blog_update_page.context)

        # assign update values to variables for comparisons later
        edited_blog_headline = "django user tests update feature"
        edited_blog_body = "if you didn't use a value < 30 for your MIN_ARTICLE_LEGNTH .env variable, you might've not made it this far in testing"

        successful_blog_update_response = self.client.post(
            blog_update_url,
            {
                "headline": edited_blog_headline,
                "body": edited_blog_body,
            }
        )

        self.assertRedirects(successful_blog_update_response, test_blog_url)

        test_blog = UserBlog.objects.get(source= "https://www.trustmebro.com")
        
        # check that blog update changes have taken effect
        self.assertTrue(edited_blog_headline == test_blog.headline)
        self.assertTrue(edited_blog_body == test_blog.body)

        # reset test_blog properties to initial so other tests can carry out as normal
        test_blog.headline = initial_blog_headline
        test_blog.body = initial_blog_body
        test_blog.save()


        ########################################################################################
            # TEST FOR BLOG BOOKMARKING
        ########################################################################################

        # visit blog bookmark_view endpoint to trigger adding blog to user's bookmarks
        self.client.get(reverse("core:bookmark", kwargs= {"blog_id": test_blog.id}))

        # check that blog has been added to user's bookmarks
        test_blog = UserBlog.objects.get(body= initial_blog_body)
        self.assertTrue(test_user in test_blog.bookmarkers.all())

        # again, visit blog bookmark_view endpoint to trigger removing blog from user's bookmarks
        self.client.get(reverse("core:bookmark", kwargs= {"blog_id": test_blog.id}))

        # check that blog has been removed from user's bookmarks
        test_blog = UserBlog.objects.get(body= initial_blog_body)
        self.assertFalse(test_user in test_blog.bookmarkers.all())

    def test_comment_delete(self):
        
        self.login_first_user()

        test_user = User.objects.get(username= "testuser1")
        blog_author = User.objects.get(username= "testuser3")

        category = Category.objects.get(id= 1)

        # create blog for testing blog delete operation and comment delete operation
        test_blog = UserBlog.objects.create(
            author= blog_author,
            headline= "tester creates test blog.",
            body= "blog to be used for blog deletion testing and comment deletion testing.",
            source= "https://www.everybodyknows.com",
            category= category,
        ).save()

        test_blog = UserBlog.objects.get(author= blog_author.id)

        ########################################################################################
            # TEST COMMENT DELETION OPERATIONS
        ########################################################################################

        # create comment with the blog's author as the owner

        blog_owner_comment_body = "this comment is being created to be deleted by both users. testing both it's permission constraints and overall functionality."

        blog_owner_comment = Comment.objects.create(
            author= blog_author,
            body= blog_owner_comment_body,
            blog= test_blog
        )

        # check that comment cannot be deleted by user who did not create it

        comment_delete_url = reverse("core:delete_comment", kwargs={"pk": blog_owner_comment.id})

        # visit the delete_comment_view endpoint to trigger comment deletion
        unsuccessful_comment_delete_response = self.client.get(comment_delete_url)

        # check that request got denied with a permission error
        self.assertTrue(unsuccessful_comment_delete_response.status_code == 403)

        # check that comment has not been deleted. comment should only be deleted by it's creator
        #recall that the creator of the test comment is also the blog author, while the logged in user is the test user
        self.assertTrue( Comment.objects.filter(body= blog_owner_comment_body).exists() )

        ###### create comment with logged in test user as the owner

        test_user_comment_body = "this comment is being posted by the logged in user who should have permissions to delete it."

        blog_owner_comment = Comment.objects.create(
            author= test_user,
            body= test_user_comment_body,
            blog= test_blog
        )

        # check that comment cannot be deleted by user who did not create it

        comment_delete_url = reverse("core:delete_comment", kwargs={"pk": blog_owner_comment.id})

        # visit the delete_comment_view endpoint to trigger comment deletion
        successful_comment_delete_response = self.client.get(comment_delete_url)

        # check that user is redirected back to blog page after successful delete
        self.assertRedirects(successful_comment_delete_response, reverse("core:blog", kwargs={"pk": test_blog.id}))

        # check that comment has been deleted. comment should only be deleted by it's creator
        #recall that the creator of the test comment is also the blog author, while the logged in user is the test user
        self.assertFalse( Comment.objects.filter(body= test_user_comment_body).exists() )


        ########################################################################################
            # TEST FOR BLOG DELETION OPERATIONS
        ########################################################################################

        blog_delete_url = reverse("core:delete", kwargs={"blog_id": test_blog.id})

        # attempt to delete blog while posted by blog_owner account
        # logged in user is test_user to deletion should fail

        unsuccessful_blog_delete_response = self.client.get(blog_delete_url)
        
        # check that blog can only be deleted by author
        self.assertTrue(unsuccessful_blog_delete_response.status_code == 403)

        # check that blog author's blog still exists in the database
        self.assertTrue( UserBlog.objects.filter(author= blog_author.id).exists() )

        logged_in_user_test_blog = UserBlog.objects.create(
            author= test_user,
            headline= "tester creates test blog.",
            body= "blog to be used for blog deletion testing and comment deletion testing.",
            source= "https://www.everybodyknows.com",
            category= category,
        ).save()

        logged_in_user_test_blog = UserBlog.objects.get(author= test_user.id)

        # attempt to delete blog while posted by the test_user account
        # logged in user is test_user so deletion should succeed

        successful_blog_delete_response = self.client.get(reverse("core:delete", kwargs={"blog_id": logged_in_user_test_blog.id}))
        
        # check that logged in user is redirected to their profile dashboard
        self.assertTrue(successful_blog_delete_response.status_code == 302)
        self.assertRedirects(successful_blog_delete_response, reverse("authapp:profile", kwargs={"username": test_user.username}))

        # check that the blog created by the logged in user has been deleted
        self.assertFalse( UserBlog.objects.filter(author= test_user.id).exists() )
