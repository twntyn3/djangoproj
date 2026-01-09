from django.urls import path
from .views import Index, SignIn, SignOut, EditReview, DeleteReview, music_page

urlpatterns = [
    path('login/', SignIn.as_view(), name='login'),
    path('logout/', SignOut.as_view(), name='logout'),
    path('', Index.as_view(), name='index'),
    path('edit/<int:pk>/', EditReview.as_view(), name='edit'),
    path('delete/<int:pk>/', DeleteReview.as_view(), name='delete'),
    path('music/', music_page, name='music'),
]
