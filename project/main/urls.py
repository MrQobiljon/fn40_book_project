from django.urls import path

from .views import (home, book_detail, book_by_category, add_book, update_book,
                    delete_book, save_comment)


urlpatterns = [
    path('', home, name='home'),
    path('books/<int:book_id>/', book_detail, name='detail'),
    path('books/<int:book_id>/update/', update_book, name='update_book'),
    path('books/<int:book_id>/delete/', delete_book, name='delete_book'),
    path('books/add/', add_book, name='add_book'),

    path('books/<int:book_id>/comment/add/', save_comment, name='save_comment'),

    path('categories/<int:category_id>/', book_by_category, name='book_by_category'),
]