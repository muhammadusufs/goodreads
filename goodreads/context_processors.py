from users.models import FriendRequest

def get_friend_request(request):
    if request.user.is_authenticated:
        amount = FriendRequest.objects.filter(to_user=request.user).count()
        return {'amount':amount}
    else:
        return {'amount':0}