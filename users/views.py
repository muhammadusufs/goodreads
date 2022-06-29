from django.dispatch import receiver
from django.shortcuts import redirect, render

from users.models import CustomUser, FriendRequest
from .forms import UpdateProfile, UserCreation, UserLogin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def registerPage(request):
    form = UserCreation()
    
    if request.method == 'POST':
        form = UserCreation(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {
        'form':form
    }
    return render(request, 'users/register.html', context)

def loginPage(request):
    login_form = AuthenticationForm()
    if request.method == 'POST':
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('profile')
    return render(request, 'users/login.html', {'login_form':login_form})

@login_required(login_url='login')
def profilePage(request):
    return render(request, 'users/profile.html', {'user':request.user})

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect("login")

@login_required(login_url='login')
def updatePage(request):
    update_form = UpdateProfile(instance=request.user)
    if request.method == "POST":
        update_form = UpdateProfile(instance=request.user, data=request.POST, files=request.FILES)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, "Successfully updated :)")
            return redirect('profile')
        else:
            messages.error(request, "Something went wrong :(")
            return redirect('edit-profile')
    return render(request, 'users/edit-profile.html', {'form':update_form})

def userPage(request, username):
    try:
        user = CustomUser.objects.get(username=username)
        return render(request, 'users/profile.html', {'user':user})
    except:
        return render(request, '404.html')

@login_required(login_url='login')
def sendFriendRequest(request, username):
    if CustomUser.objects.filter(username=username).exists():
        friend = CustomUser.objects.get(username=username)
        friend_request, created = FriendRequest.objects.get_or_create(
            from_user=request.user,
            to_user=friend
        )
        
        if created:
            messages.success(request, "Successfully sent :)")
        else:
            messages.info(request, "You have already sent request :)")

    else:
        messages.error(request, "Sorry, user not found ;(")

    return redirect("user", username=username)

@login_required(login_url='login')
def friendRequestsPage(request):
    f_requests = FriendRequest.objects.filter(to_user=request.user)
    return render(request, 'users/requests.html', {'f_requests':f_requests})

@login_required(login_url='login')
def acceptFriend(request, id):
    f_request = FriendRequest.objects.get(id=id)

    if f_request and f_request.to_user == request.user:
        f_request.to_user.friends.add(f_request.from_user)
        f_request.from_user.friends.add(f_request.to_user)
        f_request.delete()
        messages.success(request, "Successfully accepted :) ")
    else:
        messages.error(request, "Something went wrong :(")
    return redirect("friend-requests")

@login_required(login_url='login')
def rejectFriend(request, id):
    f_request = FriendRequest.objects.get(id=id)

    if f_request and f_request.to_user == request.user:
        f_request.delete()
        messages.success(request, "Request deleted :) ")
    else:
        messages.error(request, "Something went wrong :(")
    return redirect("friend-requests")

@login_required(login_url='login')
def userFriends(request, username):
    try:
        user = CustomUser.objects.get(username=username)
        if user == request.user:
            u_self = True
        else:
            u_self = False
    except:
        user = False
        u_self = False
    
    if user:
        friends = user.friends.all()
    else:
        friends = False
        messages.error(request, "Can't find "+username)
    return render(request, 'users/friends.html', {'friends':friends, 'u_self':u_self})

@login_required(login_url='login')
def cancelFriendship(request, username):
    friend = CustomUser.objects.get(username=username)

    if friend:
        request.user.friends.remove(friend)
        friend.friends.remove(request.user)
        messages.success(request, "Successfully removed :) ")
    else:
        messages.error(request, "Something went wrong :(")
    return redirect("friends", username=request.user.username)