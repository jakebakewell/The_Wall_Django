from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from login_and_registration.models import User
from .models import Message, Comment


def index(request):
    return redirect('/the_wall/home')

def home(request):
    user = User.objects.get(id=request.session['userid'])
    context = {
        "all_messages": Message.objects.all(),
        "user_messages": Message.objects.filter(user=user),
        "all_comments": Comment.objects.all(),
        "user_comments": Comment.objects.filter(user=user),
        "user": user,
    }
    return render(request, 'home.html', context)

def process_message(request):
    message_errors = Message.objects.message_validator(request.POST)
    if len(message_errors) > 0:
        for key, value in message_errors.items():
            messages.error(request, value, extra_tags='message')
        return redirect('/the_wall/home')
    else:
        message = request.POST['message']
        user = User.objects.get(id=request.session['userid'])
        Message.objects.create(user=user, content=message)
        return redirect('/the_wall/home')

def process_comment(request):
    comment_errors = Comment.objects.comment_validator(request.POST)
    if len(comment_errors) > 0:
        for key, value in comment_errors.items():
            messages.error(request, value, extra_tags='comment')
        return redirect('/the_wall/home')
    else:
        comment = request.POST['comment']
        user = User.objects.get(id=request.session['userid'])
        message_id = request.POST['which_message']
        message = Message.objects.get(id=message_id)
        Comment.objects.create(user=user, message=message, content=comment)
        return redirect('/the_wall/home')

def delete_message(request, message_id):
    message = Message.objects.get(id=message_id)
    user = User.objects.get(id=request.session['userid'])
    if message.user != user:
        return redirect('/the_wall/home')
    else:
        message_to_delete = message
        message_to_delete.delete()
        return redirect('/the_wall/home')

def log_out(request):
    request.session.flush()
    return redirect('/')