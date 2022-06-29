from urllib import request
from django.test import TestCase
from users.models import CustomUser, FriendRequest
from django.urls import reverse
from django.contrib.auth import get_user

# Create your tests here.

class RegistrationTestCase(TestCase):
    def test_required_fields(self):
        response = self.client.post(
            reverse('register'),
            data={

                'first_name':'Some',
                'last_name':'CustomUser',
            }
        )
        
        self.assertFormError(response, 'form', 'password', 'This field is required.')
        self.assertFormError(response, 'form', 'username', 'This field is required.')



    def test_unique_username(self):
        self.client.post(
            reverse('register'),
            data={
                'username':'howhow',
                'first_name':'Mark',
                'password':'howgow'
            }
        )

        response = self.client.post(
            reverse('register'),
            data={
                'username':'howhow',
                'first_name':'Sam',
                'password':'kam'
            }
        )

        user_count = CustomUser.objects.count()
        user = CustomUser.objects.get(username='howhow')
        self.assertEqual(user.first_name, 'Mark')
        self.assertEqual(user_count, 1)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')

    def test_email_is_valid(self):
        response = self.client.post(
            reverse('register'),
            data={
                'username':'someuser',
                'first_name':'Some',
                'last_name':'CustomUser',
                'email':'brocode',
                'password':'something'
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

class LoginTestCase(TestCase):
    def test_successful_login(self):
        user = CustomUser.objects.create(username="yousef", first_name="Yousef", last_name="Mohammed")
        user.set_password("Coder.2004")
        user.save()

        self.client.post(
            reverse('login'),
            data={
                "username":"yousef",
                "password":"Coder.2004"
            }
        )

        logged = get_user(self.client)
        self.assertTrue(logged.is_authenticated)

    def test_wrong_crendentials(self):
        user = CustomUser.objects.create(username="yousef", first_name="Yousef", last_name="Mohammed")
        user.set_password("Coder.2004")
        user.save()

        self.client.post(
            reverse('login'),
            data={
                "username":"yousef1",
                "password":"Coder.2004"
            }
        )

        logged = get_user(self.client)
        self.assertFalse(logged.is_authenticated)


        self.client.post(
            reverse('login'),
            data={
                "username":"yousef",
                "password":"Coder.2002"
            }
        )

        logged = get_user(self.client)
        self.assertFalse(logged.is_authenticated)

class TestProfilePage(TestCase):
    def test_login_required(self):

        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login")+'?next=/users/profile/')

    def test_profile_details(self):
        user = CustomUser.objects.create(
            username="rakhimov",
            first_name="yousef",
            last_name="rakhimov",
            email="yousef.coder@gmail.com")
        user.set_password("Coder.2022")
        user.save()

        self.client.login(username="rakhimov", password="Coder.2022")

        response = self.client.get(reverse("profile"))
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)


    def test_logout_user(self):
        user = CustomUser.objects.create(
            username="rakhimov",
            first_name="yousef",
            last_name="rakhimov",
            email="yousef.coder@gmail.com")
        user.set_password("Coder.2022")
        user.save()

        self.client.login(username="rakhimov", password="Coder.2022")

        self.client.get(reverse("logout"))

        l_user = get_user(self.client)
        self.assertFalse(l_user.is_authenticated)

    def test_profile_update(self):
        user = CustomUser.objects.create(
            username="rakhimov",
            first_name="yousef",
            last_name="rakhimov",
            email="yousef.coder@gmail.com")
        user.set_password("Coder.2022")
        user.save()

        self.client.login(username="rakhimov", password="Coder.2022")

        response = self.client.post(
            reverse("edit-profile"),
            data={
                "username":"rakhimov",
                "first_name":"Yousef",
                "last_name":"Rahimov",
                "email":"coder.yousef@gmail.com"
            }
        )

        new_user = CustomUser.objects.get(id=user.id)
        self.assertEqual(new_user.first_name, "Yousef")
        self.assertEqual(new_user.last_name, "Rahimov")
        self.assertEqual(new_user.email, "coder.yousef@gmail.com")
        self.assertEqual(response.url, reverse("profile"))


class FriendRequestsTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="defaultuser", first_name="Tester", last_name="Testov", email="testing@mail.com")
        self.user.set_password('testpass')
        self.user.save()

    def test_send_request(self):
        friend = CustomUser.objects.create(username="testfriend")
        friend.set_password("SomePass")
        friend.save()

        self.client.login(username=self.user.username, password="testpass")
        response = self.client.get(reverse("friend-request", kwargs={"username":friend.username}))

        friend_request = FriendRequest.objects.filter(from_user=self.user, to_user=friend)
        
        self.assertEqual(friend_request.count(), 1)
        self.assertEqual(friend_request[0].from_user, self.user)
        self.assertEqual(friend_request[0].to_user, friend)

    def test_without_login_send_request(self):
        friend = CustomUser.objects.create(username="testfriend")
        friend.set_password("SomePass")
        friend.save()

        response = self.client.get(reverse("friend-request", kwargs={"username":friend.username}))
        self.assertEqual(response.url, reverse("login")+'?next=/users/testfriend/send-request/')

    def test_show_friend_requests(self):
        friend = CustomUser.objects.create(username="testfriend")
        friend.set_password("SomePass")
        friend.save()

        self.client.login(username=friend.username, password="SomePass")
        friend_request = FriendRequest.objects.create(from_user=self.user, to_user=friend)
        
        response = self.client.get(reverse("friend-requests"))

        self.assertContains(response, self.user.username)

    def test_accept_friend(self):
        friend = CustomUser.objects.create(username="testfriend")
        friend.set_password("SomePass")
        friend.save()

        self.client.login(username=friend.username, password="SomePass")
        friend_request = FriendRequest.objects.create(from_user=self.user, to_user=friend)

        repsonse = self.client.get(reverse('accept-friend', kwargs={"id":friend_request.id}))

        self.assertIn(friend, self.user.friends.all())
        self.assertIn(self.user, friend.friends.all())

    def test_reject_friend(self):
        friend = CustomUser.objects.create(username="testfriend")
        friend.set_password("SomePass")
        friend.save()

        self.client.login(username=friend.username, password="SomePass")
        friend_request = FriendRequest.objects.create(from_user=self.user, to_user=friend)

        repsonse = self.client.get(reverse('delete-friend', kwargs={"id":friend_request.id}))

        self.assertNotIn(friend, self.user.friends.all())
        self.assertNotIn(self.user, friend.friends.all())
        self.assertFalse(FriendRequest.objects.filter(id=friend_request.id).exists())