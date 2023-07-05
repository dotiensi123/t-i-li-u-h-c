from django.shortcuts import render, get_object_or_404, redirect
from .models import Author
from books.models import Book
from .forms import AuthorForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

def all_authors(request):
    authors = Author.objects.all()
    return render(request, 'all_authors.html', {'authors': authors})

def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, 'author_detail.html', {'author': author})

@login_required(login_url='User:login')
@user_passes_test(lambda user: user.is_superuser)
def author_create(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('authors:all_authors')
    else:
        form = AuthorForm()
    return render(request, 'author_form.html', {'form': form, 'type': 'Create'})


@login_required(login_url='User:login')
@user_passes_test(lambda user: user.is_superuser)
def author_update(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('authors:all_authors')
    else:
        form = AuthorForm(instance=author)
    return render(request, 'author_form.html', {'form': form, 'type': 'Update'})


def author_book(request, id):
    author = Author.objects.filter(id=id)
    books = Book.objects.filter(author_id=id)
    return render(request, 'book_list.html', {'author': author, 'books': books})
    