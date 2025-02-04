from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Conversation

from .forms import ChatForm

# Create your views here.

@login_required()
def inboxview(request):
    convos = Conversation.objects.filter(slugs__in= [request.user.id])
    print(convos)
    return render(request, "inbox.html", {"conversations": convos})

@login_required()
def sendtextview(request, pk):
    slug = get_object_or_404(User, pk=pk)
    try:
        conversation = Conversation.objects.filter(slugs__in = [request.user.id,]).get(slugs__in= [slug.id,])
    except:
        print('failed')
        conversation = Conversation.objects.create()
        conversation.save()
        print('saved')
        conversation.slugs.add(get_object_or_404(User, id=pk))
        conversation.slugs.add(request.user)
        conversation.save()
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            message = form.save(commit= False)
            message.sender = request.user
            message.conversation= conversation
            conversation.save()
            message.save()
    else:
        form = ChatForm()
    return render(request, 'chat.html', {'form': form, 'conversation': conversation})

# def convo(request, pk)
#     return render(request, 'chat.html', {'form': form, 'conversation': conversation})