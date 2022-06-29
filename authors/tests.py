from django.test import TestCase
from django.urls import reverse

from books.models import Author, Book, BookAuthor

# Create your tests here.
class AuthorPageTestCase(TestCase):
    def test_author_info(self):
        author = Author.objects.create(
            first_name = "Test",
            last_name = "Last",
            email="boo@mail.com",
            bio = "Big bio"
        )
        book = Book.objects.create(title="Book", description="description", isbn="0000")
        BookAuthor.objects.create(author=author, book=book)

        response = self.client.get(reverse("author", kwargs={"id":author.id}))

        self.assertContains(response, author.first_name)
        self.assertContains(response, author.last_name)
        self.assertContains(response, author.email)
        self.assertContains(response, author.bio)

        self.assertContains(response, book.title)

    def test_no_author(self):
        response = self.client.get(reverse("author", kwargs={"id":1}))
        self.assertContains(response, "Page Not Found")