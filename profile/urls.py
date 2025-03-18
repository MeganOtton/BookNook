from . import views
from django.urls import path

urlpatterns = [
    path('', views.ProfileDetailedView.as_view(), name='profile'),
    path('move_book/<str:booktitle>', views.move_book_to_chosen, name='move_book'),
    path('check_book_purchased/<str:booktitle>', views.check_book_ownership, name='check_book_purchased'),
]