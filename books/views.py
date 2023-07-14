from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from .models import Book,BooksFavorites, Customer,Auther,Publisher,Category,Purchase,Order,OrderDetails,Purchase
from django.shortcuts import  render, redirect
from django.contrib.auth import login,logout ,authenticate
from django.contrib import messages
from decimal import Decimal
from django.utils import timezone

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/books")
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('books:book_list')
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة.')
    return render(request, 'registration/login.html')
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form)  # Check the form object in the console

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('books:book_list'))
        else:
            print(form.errors)  # طباعة تفاصيل الأخطاء في البيانات المدخلة
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
def get_similar_books(book_id):
   

    # استعراض الكتاب الحالي
    current_book = Book.objects.get(id=book_id)

    # استعراض جميع الكتب ما عدا الكتاب الحالي
    all_books = Book.objects.exclude(id=book_id)

    # استخراج النصوص من جميع الكتب
    book_texts = [book.description for book in all_books]

    # تحويل النصوص إلى مصفوفة Tfidf
    vectorizer = TfidfVectorizer(max_features=1000)  # قم بتحديد max_features وفقًا لاحتياجاتك
    tfidf_matrix = vectorizer.fit_transform(book_texts)

    # تطبيق خوارزمية K-means Clustering
    kmeans = KMeans(n_clusters=5, random_state=0)
    kmeans.fit(tfidf_matrix)

    # تحديد المراكز المشتركة للعناقيد
    cluster_centers = kmeans.cluster_centers_

    # تحديد العنقود الذي ينتمي إليه الكتاب الحالي
    current_cluster = kmeans.predict(vectorizer.transform([current_book.description]))

    # تحديد العناقيد لكل كتاب
    clusters = kmeans.labels_
    for i, cluster in enumerate(clusters):
        book = all_books[i]
        book.cluster = cluster
        book.save()

    # الكتب المشابهة في نفس العنقودة
    similar_books = Book.objects.filter(cluster=current_cluster).exclude(id=book_id)

    # قاموس لتخزين مسافات العناقيد
    current_cluster_distances = {}

    for book in similar_books:
        distance = np.linalg.norm(cluster_centers[current_cluster] - kmeans.transform(vectorizer.transform([book.description]))[:, current_cluster])
        current_cluster_distances[book.id] = distance

    # الكتب المشابهة مرتبة حسب المسافة
    similar_books = sorted(similar_books, key=lambda book: current_cluster_distances[book.id])[:5]

    return similar_books




@login_required
def favorite_book(request, book_id):
    if request.method == 'POST':
        favorite_option = request.POST.get('favorite_option')
        
        book = get_object_or_404(Book, pk=book_id)

        try:
            customer = Customer.objects.get(user=request.user)
            book_favorite, created = BooksFavorites.objects.get_or_create(
                customer=customer,
                book=book,
                defaults={
                    'is_favorite': favorite_option == 'important',
                    'is_blocked': favorite_option == 'excluded',
                }
            )
            
            if not created:
                if favorite_option == 'important':
                    book_favorite.is_favorite = True
                    book_favorite.is_blocked = False
                elif favorite_option == 'excluded':
                    book_favorite.is_favorite = False
                    book_favorite.is_blocked = True
                else:
                    book_favorite.is_favorite = False
                    book_favorite.is_blocked = False
                
                book_favorite.save()
        except Customer.DoesNotExist:
            customer = Customer.objects.create(user=request.user)
            book_favorite = BooksFavorites.objects.create(
                customer=customer,
                book=book,
                is_favorite=favorite_option == 'important',
                is_blocked=favorite_option == 'excluded',
            )
        
        return redirect('books:book_list')
    
    return redirect('login')


from django.shortcuts import render
from .models import Book, BooksFavorites
@login_required
def book_list(request):
    email = None
    if request.user.is_authenticated:
        email = request.user.email
    
    books = Book.objects.all()
    
    # Retrieve the Customer object for the authenticated user
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        customer = None
    
    # Retrieve book_favorite objects for the customer
    if customer:
        book_favorites = BooksFavorites.objects.filter(customer=customer)
        book_favorite_ids = book_favorites.values_list('book__id', flat=True)
    else:
        book_favorites = None
        book_favorite_ids = []
    
    context = {
        'books': books,
        'email': email,
        'book_favorites': book_favorites,
        'book_favorite_ids': book_favorite_ids,  # Pass the book_favorite_ids to the template
    }
    
    return render(request, 'books/book_list.html', context)


def home(request):
    return render(request,"home.html")


import pandas as pd

def import_books(request):
    dataset_path = 'books/static/books.csv'  # تحديد المسار الصحيح لملف مجموعة البيانات

    # قراءة ملف CSV وتحويله إلى قائمة من القواميس
    data_list = pd.read_csv(dataset_path).to_dict('records')

    for data in data_list:
        # استخراج المعلومات من مجموعة البيانات
        title = data['title']
        author_name = data['author']
        publisher_name = data['publisher']
        isbn = data['isbn']
        edition = data['edition']
        category_name = data['category']
        language = data['language']
        publication_date = data['publication_date']
        audience = data['audience']
        page_count_str = data['page_count']
        if data['is_series']=='نعم':
            is_series=True
        elif data['is_series']=='لا':
            is_series=False
        # is_series = data['is_series']
        series = data['series']
        format = data['format']
        price_str = data['price']
        description = data['description']
        image = data['image']

        # تحويل عدد الصفحات إلى عدد صحيح
        page_count = int(page_count_str) if page_count_str else 0

        # تحويل السعر إلى عدد عشري
        price = Decimal(price_str) if price_str else Decimal('0')

        # الحصول على الكاتب باستخدام الاسم
        author, _ = Auther.objects.get_or_create(name=author_name)

        # الحصول على الناشر باستخدام الاسم
        publisher, _ = Publisher.objects.get_or_create(name=publisher_name)

        # الحصول على التصنيف باستخدام الاسم
        category, _ = Category.objects.get_or_create(Name=category_name)

        # إنشاء سجل جديد في نموذج Book
        book = Book.objects.create(
            title=title,
            author=author,
            description=description,
            price=price,
            publication_date=publication_date,
            audience=audience,
            page_count=page_count,
            publisher=publisher,
            is_series=is_series,
            series=series,
            isbn=isbn,
            edition=edition,
            category=category,
            format=format,
            language=language,
            image=image
        )

    # عرض رسالة تأكيد بنجاح إدخال الكتب
    return HttpResponse('تم إدخال الكتب بنجاح.')

def purchase_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        purchaser_name = request.POST.get('purchaser_name')

        try:
            customer = Customer.objects.get(user=request.user.id)

            order = Order.objects.create(order_date=timezone.now(), customer=customer)
            order_details = OrderDetails.objects.create(order=order, book=book)

            purchase = Purchase.objects.create(book=book,customer=customer, purchaser_name=purchaser_name)

            return render(request, 'books/purchase_success.html', {'purchase': purchase})
        except (Customer.DoesNotExist):
            # معالجة خطأ في حالة عدم وجود العميل
            return redirect('books:book_list')

    # إرجاع النموذج في حالة طلب GET
    return render(request, 'books/purchase_book.html', {'book': book})
def purchase_list(request):
    if request.user.is_authenticated:
        purchases = Purchase.objects.filter(customer__user=request.user)
        return render(request, 'books/purchase_list.html', {'purchases': purchases})
    else:
        # يمكنك تنفيذ سلوك آخر إذا لم يكن المستخدم مسجل الدخول
        return render(request, 'books/not_authenticated.html')

from django.shortcuts import render
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from .models import Purchase, Book


from apyori import apriori

def get_purchased_books(book_id):
    # استعراض الكتاب الحالي
    current_book = Book.objects.get(id=book_id)

    # البحث عن العملاء الذين قاموا بشراء الكتاب الحالي
    customers = Customer.objects.filter(order__orderdetails__book=current_book)

    # الحصول على قائمة الكتب المشتراة من قبل هؤلاء العملاء
    purchased_books = Book.objects.filter(orderdetails__customer__in=customers)

    # تحويل الكتب المشتراة إلى قائمة
    purchased_books_list = [book.title for book in purchased_books]

    # استخدام خوارزمية Apriori للحصول على القواعد المشتركة
    rules = apriori(purchased_books_list, min_support=0.1, min_confidence=0.5)

    return list(rules)




@login_required
def book_detail(request, book_id):
    # استعراض الكتاب الحالي
    current_book = Book.objects.get(id=book_id)

    # استرداد الكتب المشابهة
    similar_books = get_similar_books(current_book.id)
    # الحصول على الكتب المشتراة
    purchased_books = get_purchased_books(book_id)

    return render(request, 'books/book_detail.html', {'current_book':current_book,'similar_books':similar_books,'purchased_books':purchased_books})
