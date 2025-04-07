from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Conversation, SlugMessages



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
        

        
    def login_first_user(self):
        self.client.login(username= "test1@user.com", password= "AA@@bb11")

    def test_inbox_view(self):

        self.login_first_user()

        allowed_inbox_types = ["all", "archived"]

        for inbox_type in allowed_inbox_types:
            inbox_page = self.client.get(reverse("messagesapp:inbox", kwargs= {"inbox_type": inbox_type}))
            self.assertTemplateUsed(inbox_page, "inbox.html")

            # check that the chat page template is loaded with the necessary data
            expected_context_data = ["conversations", "inbox_type", "inbox_toggle"]

            for context in expected_context_data:
                self.assertTrue(context in inbox_page.context)


    
    def test_sequence_start_chat_send_message_archive_chat_unarchive(self):
        """
            test for checking that a conversation is initiated properly
        """
        # login to allow access to view endpoints and for proper conversation configurations
        self.login_first_user()

        logged_in_user = User.objects.get(username= "testuser1")
        blogger = User.objects.get(username= "testuser3")

        # set variable to conversation url including the reciever: blogger's username as the parameter
        chat_url = reverse("messagesapp:send", kwargs={"username": blogger.username})

        ########################################################################################
            # TEST FOR STARTING CHAT
        #######################################################################################

        # confirm that no conversation already exists in the database between the necessary parties
        self.assertFalse( Conversation.objects.filter(slugs__in= [logged_in_user.id, blogger.id]).exists() )

        # visit send_text_view endpoint to trigger starting a conversation between the logged_in_user and blogger
        chat_page = self.client.get(chat_url)
        self.assertTemplateUsed(chat_page, "chat.html")

        # check that a conversation object has been created in the database between the necessary parties
        self.assertTrue( Conversation.objects.filter(slugs__in= [logged_in_user.id, blogger.id]).exists() )
        
        # check that the chat page template is loaded with the necessary data
        expected_context_data = ["form", "conversation", "friend_name"]

        for context in expected_context_data:
            self.assertTrue(context in chat_page.context)

        ########################################################################################
            # TEST FOR SENDING MESSAGE IN CHAT
        ########################################################################################
        
        message_body = "hello, blogger. this is logged_in_user texting"

        successful_message_sent_response = self.client.post(
            chat_url,
            {
                "text": message_body
            }
        )
        
        #check that message was sent and exists in database

        chat_object = Conversation.objects.filter(slugs__in= [logged_in_user.id, blogger.id])[0]

        
        self.assertTrue( chat_object.messages.filter(text= message_body).exists() )

        self.assertTrue( chat_object.messages.get(text= message_body).sender )


        ########################################################################################
            # TEST FOR ARCHIVING CHAT
        #######################################################################################

        # visit archive_chat_view endpoint to trigger chat archiving

        archive_chat_url = reverse("messagesapp:archive", kwargs={"id": chat_object.id})

        successful_archive_action_response = self.client.get(archive_chat_url)
        self.assertRedirects(successful_archive_action_response, reverse("messagesapp:inbox", kwargs={"inbox_type": "all"}))

        # check that a conversation has been archived on the logged in user's end

        chat_object = Conversation.objects.filter(slugs__in= [logged_in_user.id, blogger.id])[0]

        # confirm that logged in user is a member of that chat
        self.assertTrue( logged_in_user in chat_object.disengaged.all())
        self.assertTrue(logged_in_user in chat_object.slugs.all())
        self.assertTrue( blogger not in chat_object.disengaged.all())

        # check that an indicator message has been created inside to conversation to signal users
        # chat has been archived
        self.assertTrue(chat_object.messages.filter(is_indicator_message= True).exists())

        # visit send_text_view endpoint to unarchive conversation between the logged_in_user and blogger
        chat_page = self.client.get(chat_url)
        self.assertTemplateUsed(chat_page, "chat.html")

        # check that a conversation has been archived on the logged in user's end

        chat_object = Conversation.objects.filter(slugs__in= [logged_in_user.id, blogger.id])[0]
                
        # confirm that logged in user is now engaged in chat
        self.assertTrue( logged_in_user not in chat_object.disengaged.all() )
        # confirm that blogger is still engaged in chat
        self.assertTrue( blogger not in chat_object.disengaged.all() )

        # check that a second indicator message has been created inside to conversation to signal users
        # chat has been opened
        # so far 3 indicator messages chould have been created for starting chat, closing chat, and re-opening chat.

        self.assertTrue(len(chat_object.messages.filter(is_indicator_message= True)) == 3 )