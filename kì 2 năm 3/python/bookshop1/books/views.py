from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Book
from bookreviews.models import BookReview
from .forms import BookForm
from django.db.models import Q
from django.urls import reverse
from bookreviews.forms import BookReviewForm
from django.db.models import Avg
from django.contrib.auth.decorators import user_passes_test

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = BookReview.objects.filter(book=book)
    
    return render(request, 'book_detail.html', {'book': book, 'reviews': reviews})
def book_list(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'book_list.html', context)

@login_required(login_url='users:login')
@user_passes_test(lambda user: user.is_superuser)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST,request.FILES)
        if form.is_valid():
            book = form.save()
            return redirect('books:book_detail', pk=book.pk)
    else:
        form = BookForm()
    context = {'form': form}
    return render(request, 'book_create.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = BookReview.objects.filter(book=book)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    return render(request, 'book_detail.html', {'book': book, 'reviews': reviews, 'avg_rating': avg_rating})

@login_required(login_url='users:login')
@user_passes_test(lambda user: user.is_superuser)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            return redirect('books:book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    context = {'form': form}
    return render(request, 'book_edit.html', context)

@login_required(login_url='users:login')
@user_passes_test(lambda user: user.is_superuser)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('books:book_list')
    context = {'book': book}
    return render(request, 'book_delete.html', context)

# | Book.objects.filter(author__name__icontains=query) 
def book_search(request):
    query = request.GET.get('query')
    if query:
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__name__icontains=query) | Book.objects.filter(genre__name__icontains=query) 
        context = {
            'books': books,
        }
        return render(request, 'book_list.html', context) # Trả về trang kết quả
    else:
        return render(request, 'book_list.html') # Trả về trang search nếu không có query

