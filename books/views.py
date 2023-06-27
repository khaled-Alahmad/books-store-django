from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from .models import Book,BooksFavorites, Customer
from django.shortcuts import  render, redirect
from django.contrib.auth import login,logout ,authenticate
from django.contrib import messages

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


@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    purchased_books = book.purchase_set.all()
    similar_books = book.similar_books.all()
    return render(request, 'books/book_detail.html', {'book': book, 'purchased_books': purchased_books, 'similar_books': similar_books})

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