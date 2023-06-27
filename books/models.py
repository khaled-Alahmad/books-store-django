from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer')
    def __str__(self):
      return self.user.username   
    

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    order_date=models.DateField()
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,default="")




class Auther(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default="")

    def __str__(self):
        return self.user.username   
class Publisher(models.Model):
    id = models.AutoField(primary_key=True)
    Name=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.Name   



class Category(models.Model): 
    id = models.AutoField(primary_key=True)
    Name=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.Name    


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Auther,on_delete=models.CASCADE,default="")
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    publication_date = models.CharField(max_length=4)  # تخزين السنة فقط
    audience = models.CharField(max_length=100)
    page_count = models.IntegerField()
    publisher = models.ForeignKey(Publisher,on_delete=models.CASCADE,default="")
    series = models.CharField(max_length=100)
    isbn = models.CharField(max_length=100)
    edition = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default="")
    format = models.CharField(max_length=100)
    language = models.CharField(max_length=100) 
    is_favorite = models.BooleanField(default=False)
    def __str__(self):
        return self.title


class OrderDetails(models.Model):
    id = models.AutoField(primary_key=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,default="")
    book=models.ForeignKey(Book,on_delete=models.CASCADE,default="", related_name='favorites')


class Purchase(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    purchaser_name = models.CharField(max_length=100)
    purchase_date = models.DateField(auto_now_add=True)


class SimilarBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='similar_books')
    similar_book = models.ForeignKey(Book, on_delete=models.CASCADE)

class BooksFavorites(models.Model):
    id = models.AutoField(primary_key=True)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,default="")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default="")

    is_favorite=models.BooleanField(default=False)
    is_blocked=models.BooleanField(default=False)
    