from django.contrib import admin
from django.urls import path,include
from books import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_request, name='logout'),
    path('accounts/register/', views.register_view, name='register'),
    path('admin/', admin.site.urls),
    path('books/', include('books.urls',namespace='books')),

]
