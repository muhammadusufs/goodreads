from django.urls import path

from api.views import get_review, get_reviews


urlpatterns = [
    path("reviews/<str:id>/", get_review, name='api-review'),
    path("reviews/", get_reviews, name='api-reviews'),
]