from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Conversation, SlugMessages
from django.core.paginator import Paginator
from django.db.models import Q
from django import http

from .forms import ChatForm

# Create your views here.

#Import custom authentication user model and assign to variable 'User'
User = get_user_model()

#view for retrieving user's active conversations
@login_required()
def inbox_view(request, inbox_type):
    if inbox_type == "all":
        inbox_toggle = "archived"
        conversations = request.user.conversations.all().filter( ~Q(disengaged__in= [request.user.id]) )
    elif inbox_type == "archived":
        inbox_toggle = "all"
        conversations = request.user.archived_conversations.all()

    else:
        return http.HttpResponseBadRequest({"message": "error. invalid url"})

    page = request.GET.get('p')

    paginator_class = Paginator(conversations, 10)
    conversations = paginator_class.get_page(page)
    
    return render(request, "inbox.html", {"conversations": conversations, "inbox_type": inbox_type, "inbox_toggle": inbox_toggle})


#view for retrieving messages of a conversation / sending messages to a participant of a conversation
@login_required()
def send_text_view(request, username):
    slug = get_object_or_404(User, username= username)
    print(request.user.id, slug.id)
    page = request.GET.get('p')

    #try to retrieve chat history between the user and the second party
    #create a new chat if there is no conversation between the two parties and add both parties to this new conversation
    try:
        conversation = Conversation.objects.filter(slugs__in = [request.user.id,]).get(slugs__in= [slug.id,])
        if request.user in conversation.disengaged.all():
            indicator_message = SlugMessages.objects.create(
            is_indicator_message= True,
            text= f"{request.user.username} has opened the chat",
            conversation= conversation,
            )
            indicator_message.save()
            conversation.disengaged.remove(request.user)
    except:
        conversation = Conversation.objects.create()
        conversation.save()

        conversation.slugs.add(get_object_or_404(User, username= username))
        conversation.slugs.add(request.user)

        conversation.save()

        indicator_message = SlugMessages.objects.create(
            is_indicator_message= True,
            text= f"{request.user.username} has started the chat",
            conversation= conversation,
        )
        indicator_message.save()

    paginated_convo = Paginator(conversation.messages.all(), 12)
    
    if page:
        conversation_page = paginated_convo.get_page(page)
    else:
        conversation_page = paginated_convo.get_page(paginated_convo.num_pages)

    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            message = form.save(commit= False)
            message.sender = request.user
            message.conversation= conversation
            conversation.save()
            message.save()
            return redirect(request.path)
    else:
        form = ChatForm()
    return render(request, 'chat.html', {'form': form, 'conversation': conversation_page, 'friend_name': username})

#view for closing a conversation
#chat history is not deleted and can be retrieved upon opening the conversation again through the second party's profile
def archive_chat_view(request, id):
    conversation = Conversation.objects.get(id= id)
    print('gotten')
    if request.user not in conversation.disengaged.all():
        indicator_message = SlugMessages.objects.create(
            is_indicator_message= True,
            text= f"{request.user.username} has closed this chat",
            conversation= conversation,
        )
        indicator_message.save()
        conversation.disengaged.add(request.user)
        print('closed')
    else:
        print('failed')
    return redirect('messagesapp:inbox', 'all')