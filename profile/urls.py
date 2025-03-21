from . import views
from django.urls import path


urlpatterns = [
    path('account/', views.account_view, name='profile'),
    path('author/', views.ProfileAuthorDetailedView.as_view(), name='profile_author'),
    path('admin/', views.ProfileAdminDetailedView.as_view(), name='profile_admin'),
    path('move_book/<str:booktitle>', views.move_book_to_chosen, name='move_book'),
    path('move_wishlist_book/<str:booktitle>', views.move_book_to_wishlist, name='move_wishlist_book'),
    path('check_book_purchased/<str:booktitle>', views.check_book_ownership, name='check_book_purchased'),
    path('signup/author/', views.AuthorSignupView.as_view(), name='account_signup_author'),
    path('library/', views.library_view, name='library'),
    path('account/', views.account_view, name='account'),
    path('hide-options/<int:item_id>/', views.hide_options, name='hide_options'),
    path('book/<slug:slug>/', views.book_details_list, name='book_details_list'),
]


