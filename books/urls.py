from django.urls import path
from . import views
app_name = 'books'

urlpatterns = [
   
    path('', views.book_list, name='book_list'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('favorite/<int:book_id>/', views.favorite_book, name='favorite_book'),
    path('recommendations/', views.book_recommendations, name='book_recommendations'),
    path('import/', views.import_books, name='import_books'),
    path('purchase/<int:book_id>/', views.purchase_book, name='purchase_book'),
    path('purchase/', views.purchase_list, name='purchase_book'),

]