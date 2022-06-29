from django import views
from django.urls import path
from .views import deleteReview, detailPage, editReview, homePage, homeReviews

urlpatterns = [
    path("", homePage, name="books"),
    path("home/", homeReviews, name="home-reviews"),
    path("<str:id>/", detailPage, name="book-detail"),
    path("<str:book>/edit-review/<str:id>", editReview, name="edit-review"),
    path("<str:book>/delete-review/<str:id>", deleteReview, name="delete-review"),

]