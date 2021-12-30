from decimal import Context
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.clickjacking import xframe_options_exempt

from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required

from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from messenger.forms import UserRegistrationForm
from django.utils import timezone

from .models import Message


def index(request):
    from django.db import connection
    context = {}

    context["username_list"] = ["all"] + [u.username for u in User.objects.all()]

    if 'filter_username' in request.session and request.session['filter_username'] != "all":
        filter_username = request.session['filter_username']
        # user_filter_id = User.objects.filter(username=filter_username)[0].id
        user_filter_id = User.objects.raw(f"SELECT id, username FROM auth_user WHERE username='{str(filter_username)}' ORDER BY id")[0].id
        message_list = Message.objects.filter(user_id=user_filter_id).order_by('sent_at')
    else:
        message_list = Message.objects.order_by('sent_at')

    context["message_list"] = message_list
    context["count"] = len(message_list)

    return render(request, 'messenger/index.html', context)


def register(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created. You can log in now!')
            return redirect('login')
    else:
        # form = UserCreationForm()
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'messenger/register.html', context)

@login_required
def new(request):
    return render(request, 'messenger/new.html')


@xframe_options_exempt
def profile(request, user_id):
    current_user = User.objects.get(id=int(user_id.split()[0]))
    html_str = '<link rel="shortcut icon" href="/static/images/favicon.png"/>\n'
    html_str = html_str + f"Showing page for user_id: {user_id}\n"
    html_str = html_str + f'<p>Username = {current_user.username} \
                            <p>First Name = {current_user.first_name} \
                            <p>Last Name = {current_user.last_name}'
    return HttpResponse(html_str)


def send(request):
    form = request.POST
    new_content = form["content"]
    current_user = request.user
    current_time = timezone.now()
    new_message = Message(content=new_content, sent_at=current_time, user=current_user)
    new_message.save()
    return redirect("/")


@csrf_exempt
def filter_messages_by_user(request):
    if request.method == 'POST':
        form = request.POST
        filter_username_ = form["username"]
        request.session['filter_username'] = filter_username_
        messages.success(request, f'User selected')
        return redirect("/")
