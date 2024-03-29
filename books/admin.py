from django.contrib import admin

from books.models import Author, Book, BookAuthor, BookReview

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'isbn')
    list_display = ('title', 'isbn', 'description')

class AuthorAdmin(admin.ModelAdmin):
    pass

class BookAuthorAdmin(admin.ModelAdmin):
    pass

class BookReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)