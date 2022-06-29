from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from .forms import BookReviewForm
from django.contrib import messages

from books.models import Book, BookReview

# Create your views here.
def homePage(request):
    books = Book.objects.all().order_by('id')
    search_query = request.GET.get('q', '')
    if search_query:
        books = Book.objects.filter(title__icontains=search_query)

    page_size = request.GET.get('page_size',2)
    page_num = request.GET.get('page', 1)

    pages = Paginator(books, page_size)
    page = pages.get_page(page_num)
    
    return render(request, 'books/landing.html', {'books':page, 'search_query':search_query})

def homeReviews(request):
    reviews = BookReview.objects.all().order_by('-created_at')
    page_size = request.GET.get('page_size', 10)
    paginator = Paginator(reviews, page_size)
    page_num = request.GET.get('page', 1)
    page_object = paginator.get_page(page_num)

    return render(request, 'books/home.html', {'page_obj':page_object})

def detailPage(request, id):
    try:
        book = Book.objects.get(id=id)
        if request.method == "POST" and request.user.is_authenticated:
            form = BookReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.book = book
                review.save()
                messages.success(request, "Successfully posted :)")
            else:
                messages.error(request, 'Something went wrong :(')

        return render(request, 'books/detail.html', {'book':book})
    except:
        return render(request, '404.html')

def editReview(request, book, id):
    try:
        review = BookReview.objects.get(id=id)
    except:
        review = False

    if request.user.is_authenticated and review and review.user == request.user:
        form = BookReviewForm(instance=review)
        if request.method == "POST":
            form = BookReviewForm(instance=review, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Updated Successfully")
                return redirect('book-detail', id=book)
            else:
                messages.error(request, "Something went wrong")
        return render(request, 'books/editreview.html', {'form':form})
    else:
        return redirect("books")

def deleteReview(request, book, id):
    try:
        review = BookReview.objects.get(id=id)
    except:
        review = False

    if request.user.is_authenticated and review and review.user == request.user:
        if request.method == "POST":
            review.delete()
            messages.success(request, "Successfully deleted :)")
            return redirect('book-detail', id=book)
        return render(request, 'books/deletereview.html')
    else:
        return redirect("books")
        
