from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from books.models import Book, BookReview

from users.models import CustomUser

class BookReviewTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="testuser",
            first_name ="Test Name",
            last_name = "Test Last",
            email = "test@mail.com"
            )
        self.user.set_password("PasswordTest")
        self.user.save()
        self.client.login(username="testuser", password="PasswordTest")

    def test_one_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123456789")
        rv = BookReview.objects.create(book=book, user=self.user, stars_given=4, comment="Cool")

        response = self.client.get(reverse("api-review", kwargs={'id':rv.id}))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['first_name'], "Test Name")
        self.assertEqual(response.data['user']['last_name'], "Test Last")
        self.assertEqual(response.data['user']['email'], "test@mail.com")

        self.assertEqual(response.data['book']['id'], book.id)
        self.assertEqual(response.data['book']['title'], 'Book1')
        self.assertEqual(response.data['book']['description'], 'Description1')
        self.assertEqual(response.data['book']['isbn'], '123456789')

        self.assertEqual(response.data['comment'], "Cool")
        self.assertEqual(response.data['stars_given'], 4)

    def test_many_reviews(self):
        user2 = CustomUser.objects.create(username="test2user") # creating second user
        book1 = Book.objects.create(title="Book1", description="Description1", isbn="123456789") # creating books
        rv1 = BookReview.objects.create(book=book1, user=self.user, stars_given=4, comment="Cool") # creating review1
        rv2 = BookReview.objects.create(book=book1, user=user2, stars_given=1, comment="Bad") # creating review2

        response = self.client.get(reverse('api-reviews')) # sending request and getting response
        
        # checking size data and status  
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['count'], 2)
        self.assertIn('previous', response.data)
        self.assertIn('next', response.data)
        self.assertEqual(response.status_code, 200)

        # checking review1 user info
        self.assertEqual(response.data['results'][0]['user']['id'], user2.id)
        # self.assertEqual(response.data['results'][0]['user']['first_name'], "Test Name")
        # self.assertEqual(response.data['results'][0]['user']['last_name'], "Test Last")
        # self.assertEqual(response.data['results'][0]['user']['email'], "test@mail.com")

        # checking review1 book info
        self.assertEqual(response.data['results'][0]['book']['id'], book1.id)
        self.assertEqual(response.data['results'][0]['book']['title'], 'Book1')
        self.assertEqual(response.data['results'][0]['book']['description'], "Description1")
        self.assertEqual(response.data['results'][0]['book']['isbn'], "123456789")

        # checking review1
        self.assertEqual(response.data['results'][1]['comment'], 'Cool')
        self.assertEqual(response.data['results'][1]['stars_given'], 4)

        # ============================================================= # 

        # checking review2 user info
        self.assertEqual(response.data['results'][1]['user']['id'], self.user.id)
        self.assertEqual(response.data['results'][1]['user']['first_name'], "Test Name")
        self.assertEqual(response.data['results'][1]['user']['last_name'], "Test Last")
        self.assertEqual(response.data['results'][1]['user']['email'], "test@mail.com")

        # checking review2 book info
        self.assertEqual(response.data['results'][1]['book']['id'], book1.id)
        self.assertEqual(response.data['results'][1]['book']['title'], 'Book1')
        self.assertEqual(response.data['results'][1]['book']['description'], "Description1")
        self.assertEqual(response.data['results'][1]['book']['isbn'], "123456789")

        # checking review2
        self.assertEqual(response.data['results'][0]['comment'], 'Bad')
        self.assertEqual(response.data['results'][0]['stars_given'], 1)

    def test_delete(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123456789") # creating book
        rv = BookReview.objects.create(book=book, user=self.user, stars_given=4, comment="Cool") # creating review

        response = self.client.delete(reverse("api-review", kwargs={"id":rv.id}))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(BookReview.objects.filter(book=book).exists(), False)

    def test_patch(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123456789") # creating book
        rv = BookReview.objects.create(book=book, user=self.user, stars_given=4, comment="Cool") # creating review

        response = self.client.patch(reverse("api-review", kwargs={"id":rv.id}), data={"comment":"Good"})

        self.assertEqual(response.status_code, 202)
        rv.refresh_from_db()
        self.assertEqual(rv.comment, "Good")

    def test_post(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123456789") # creating book

        data = {
            "book_id":book.id,
            "user_id":self.user.id,
            "stars_given":4,
            "comment":"Not Bad :)"
        }

        response = self.client.post(reverse("api-reviews"), data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['stars_given'], 4)
        self.assertEqual(response.data['comment'], "Not Bad :)")