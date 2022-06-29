from functools import partial
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.serializers import BookReviewSerializer
from rest_framework.pagination import PageNumberPagination
from books.models import BookReview

@api_view(['GET', 'DELETE', 'PATCH'])
@permission_classes([IsAuthenticated])
def get_review(request, id):

    # GET request
    if request.method == "GET":
        try:
            review = BookReview.objects.get(id=id)
            serializer = BookReviewSerializer(review)
            return Response(data=serializer.data)
        except:
            return Response('Nothing found', status=status.HTTP_404_NOT_FOUND)

    # DELETE request
    if request.method == "DELETE":
        try:
            review = BookReview.objects.get(id=id)
            review.delete()
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response('Nothing found', status=status.HTTP_404_NOT_FOUND)

    # PATCH request for UPDATE
    if request.method == "PATCH":
        try:
            review = BookReview.objects.get(id=id)
        except:
            return Response('Nothing found', status=status.HTTP_404_NOT_FOUND)

        serializer = BookReviewSerializer(instance=review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def get_reviews(request):
    reviews = BookReview.objects.all().order_by('-created_at')
    paginator = PageNumberPagination()
    page_obj = paginator.paginate_queryset(reviews, request)
    serializer = BookReviewSerializer(reviews, many=True)

    if request.method == "POST":
        serializer = BookReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return paginator.get_paginated_response(serializer.data)