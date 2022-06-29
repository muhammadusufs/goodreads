from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser
from django.contrib.auth import get_user
from .models import Author, Book, BookAuthor, BookReview
# Create your tests here.
class BookTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(
            reverse('books')
        )

        self.assertContains(response, 'No books found.')

    def test_book_list(self):
        book1 = Book.objects.create(title="Book1", description="Desc1", isbn="15161561")
        book2 = Book.objects.create(title="Book2", description="Desc1", isbn="15161561")
        book3 = Book.objects.create(title="Book3", description="Desc1", isbn="15161561")

        response = self.client.get(
            reverse("books")+"?page_size=2"
        )

        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(
            reverse("books")+"?page=2&page_size=2"
        )
        self.assertContains(response, book3.title)

    def test_book_details(self):
        book = Book.objects.create(title="Book1", description="Desc1", isbn="15161561")
        response = self.client.get(reverse("book-detail", kwargs={"id":book.id}))
        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_book_reviews(self):
        book = Book.objects.create(title="Book1", description="Desc1", isbn="15161561")
        user = CustomUser.objects.create(
            username="rakhimov",
            first_name="yousef",
            last_name="rakhimov",
            email="yousef.coder@gmail.com")
        user.set_password("Coder.2022")
        user.save()

        review1 = BookReview.objects.create(user=user, book=book, stars_given=3, comment="Very")
        review2 = BookReview.objects.create(user=user, book=book, stars_given=2, comment="Good Book")
        review3 = BookReview.objects.create(user=user, book=book, stars_given=5, comment="Nice")

        response = self.client.get(reverse("home-reviews") + '?page_size=2')

        self.assertContains(response, review2.comment)
        self.assertContains(response, review1.comment)


    def test_book_authors(self):
        book = Book.objects.create(title="Book1", description="Desc1", isbn="15161561")
        author1 = Author.objects.create(
            first_name = "Mohammed Yousef",
            last_name = "Rakhimov",
            email = "mohammedyousefs@gmail.com",
            bio = "No bio"
        )

        author2 = Author.objects.create(
            first_name = "Abdurrohman",
            last_name = "Rakhimov",
            email = "abdurrohmans@gmail.com",
            bio = "No bio"
        )

        bookauthor1 = BookAuthor.objects.create(book=book, author=author1)
        bookauthor2 = BookAuthor.objects.create(book=book, author=author2)
        
        response =  self.client.get(reverse('book-detail', kwargs={"id":book.id}))

        self.assertContains(response, bookauthor1.author.first_name)
        self.assertContains(response, bookauthor2.author.first_name)

 
        