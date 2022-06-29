from django.urls import path

from users.views import acceptFriend, cancelFriendship, friendRequestsPage, profilePage, registerPage, loginPage, logoutPage, rejectFriend, sendFriendRequest, updatePage, userFriends, userPage

urlpatterns = [
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutPage, name='logout'),
    path("profile/", profilePage, name='profile'),
    path("edit-profile/", updatePage, name='edit-profile'),

    path("friends/<str:username>/", userFriends, name='friends'),
    path("friend-requests/", friendRequestsPage, name='friend-requests'),
    path("accept-friend/<str:id>/", acceptFriend, name='accept-friend'),
    path("delete-friend/<str:id>/", rejectFriend, name='delete-friend'),
    path("cancel-friend/<str:username>/", cancelFriendship, name='cancel-friend'),
    path("<str:username>/", userPage, name='user'),
    path("<str:username>/send-request/", sendFriendRequest, name='friend-request'),

]