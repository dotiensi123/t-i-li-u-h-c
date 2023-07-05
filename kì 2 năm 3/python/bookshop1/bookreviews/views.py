from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BookReview
from .forms import BookReviewForm
from books.models import Book
from django.urls import reverse
from django.db.models import Avg

@login_required
def create_review(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('books:book_detail', book.pk)
    else:
        form = BookReviewForm()
    return render(request, 'create_review.html', {'book': book, 'form': form})

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(BookReview, pk=review_id)
    if review.user != request.user:
        return redirect('books:book_detail', pk=review.book.id)
    if request.method == 'POST':
        form = BookReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('books:book_detail', pk=review.book.id)
    else:
        form = BookReviewForm(instance=review)
    return render(request, 'edit_review.html', {'form': form, 'review': review})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(BookReview, pk=review_id)
    if review.user != request.user:
        return redirect('books:book_detail', pk=review.book.id)
    review.delete()
    return redirect('books:book_detail', pk=review.book.id)

def top_rated_books(request):
    # Sắp xếp các cuốn sách theo thứ tự giảm dần của trung bình rating và lấy ra 10 cuốn sách đầu tiên
    books = Book.objects.annotate(avg_rating=Avg('bookreview__rating')).order_by('-avg_rating')[:10]
    return render(request, 'book_list.html', {'books': books})
