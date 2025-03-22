from . import views
from django.urls import path
from .views import device_detection_view, BookList

urlpatterns = [
    path('', device_detection_view, name='device_detection'),
    path('index/', BookList.as_view(), name='index'),  # Assuming BookList is your index view
    path('search/', views.BookListSearch.as_view(), name='book_search'),
    path('<slug:slug>/', views.book_details, name='book_details_list'),
    # path('<slug:slug>/', views.book_details, name='book_wishlist_list'),
    path('review/<int:id>/', views.review_detail, name='review_detail'),
    path('<slug:slug>/edit_comment/<int:comment_id>', views.comment_edit, name='comment_edit'),
    path('<slug:slug>/delete_comment/<int:comment_id>', views.comment_delete, name='comment_delete'),
    path('api/save-device-type/', views.save_device_type, name='save_device_type'),
]