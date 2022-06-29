from email.policy import default
from django.utils import timezone
from django.db import models
from users.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    isbn = models.CharField(max_length=17)
    cover_pic = models.ImageField(default='cover.png')

    def __str__(self):
        return self.title

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()
    pic = models.ImageField(default='rasm.jpg')

    def __str__(self):
        return f"{self.first_name}  {self.last_name}"

class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book.title} by {self.author}"

    def fullname(self):
        return f"{self.author}"

class BookReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.TextField()
    stars_given = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.stars_given} by {self.user.username}"