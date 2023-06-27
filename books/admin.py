from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(Book)
admin.site.register(Auther)
admin.site.register(Customer)
admin.site.register(Publisher)
admin.site.register(Order)
admin.site.register(BooksFavorites)
admin.site.register(Category)
admin.site.register(OrderDetails)
admin.site.register(Purchase)
admin.site.register(SimilarBook)
