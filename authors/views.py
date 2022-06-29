from django.shortcuts import render

from books.models import Author

# Create your views here.
def authorPage(request, id):
    try:
        author = Author.objects.get(id=id)
        authorBooks = author.bookauthor_set.all()

        reviews = 0
        for bookReview in authorBooks:
            reviews += bookReview.book.bookreview_set.all().count()

        return render(request, 'authors/authorpage.html', {'author':author, 'reviews':reviews})
    except:
        return render(request, '404.html')