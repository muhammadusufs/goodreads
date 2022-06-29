from django.urls import path

from authors.views import authorPage


urlpatterns = [
    path("<str:id>/", authorPage, name='author')
]