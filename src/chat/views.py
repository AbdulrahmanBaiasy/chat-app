import json
from django.contrib import messages 
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Room
from account.forms import AddUserForm, EditUserForm
from account.models import User

# Create your views here.
@require_POST
def create_room(request, uuid):
    name = request.POST.get("name", "")
    url = request.POST.get("url", "")
    Room.objects.create(uuid=uuid, client=name, url=url)
    return JsonResponse({"message": "room_created"})


@login_required
def admin(request):
    rooms = Room.objects.all()
    users = User.objects.filter(is_staff=True)
    context= {
        'users':users, 
        'rooms': rooms
    }
    return render(request, "chat/admin.html", context)


@login_required
def room(request, uuid): 
    room = Room.objects.get(uuid=uuid)
    if room.status == Room.WAITING : 
        room.status = Room.ACTIVE
        room.agent = request.user 
        room.save()
    return render (request, 'chat/room.html',{
        'room': room
    } )


@login_required
def add_user(request):
    if request.user.has_perm('user.add_user'):
        if request.method == 'POST':
            form = AddUserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_staff = True
                user.set_password(request.POST.get('password'))
                user.save()
                if user.role == User.MANAGER: 
                    group = Group.objects.get(name='Managers')
                    group.user_set.add(user)
                messages.success(request, 'The user was added!')
                return redirect('/chat-admin/')
        else:
            form = AddUserForm()
        return render(request, 'chat/add_user.html', {
            'form': form
        })
    else:
        print("no perm")
        messages.error(request, 'You don\'t have access to add users!')

        return redirect('/chat-admin/')
        
@login_required
def user_detail(request, uuid):
    user= User.objects.get(pk= uuid)
    rooms =user.rooms.all()
    context = {
        'user': user ,
        'rooms': rooms
    }
    return render (request, 'chat/user_detail.html', context)

@login_required
def rooms(request):
    rooms = Room.objects.order_by("status")
    context = {
        "rooms": rooms
    }
    return render (request, "chat/rooms.html" , context)





        
@login_required
def edit_user(request, uuid):
    if request.user.has_perm('user.edit_user'):
        user = User.objects.get(pk=uuid)
        print('HAS PERM')
        if request.method == 'POST':
            print('post method before ')
            form = EditUserForm(request.POST, instance=user)
            print('post method after ')

            if form.is_valid():
                print('valid')
                form.save()
                messages.success(request, 'The changes was saved!')
                return redirect('/chat-admin/')
            else: 
                print('not valid')
        else:
            form = EditUserForm(instance=user)
        context= { 
            'user': user,
            'form': form
        }
        return render(request, 'chat/edit_user.html',context)
    else:
        messages.error(request, 'You don\'t have access to edit users!')

        return redirect('/chat-admin/')

@login_required
def delete_room(request, uuid):
    if request.user.has_perm('room.delete_room'):
        room = Room.objects.get(uuid=uuid)
        room.delete()
        messages.success(request, 'room was deleted')
        return redirect('/chat-admin/')
    else : 
        messages.error(request, 'you don\'t have access to delete users')
        return redirect ('/chat-admin/')