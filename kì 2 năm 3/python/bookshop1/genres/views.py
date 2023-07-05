from django.shortcuts import render, redirect
from .models import Genres
from books.models import Book
from .forms import GenreForm

def all_genres(request):
    genres = Genres.objects.all()
    context = {'genres': genres}
    return render(request, 'all_genres.html', context)

def genre_create(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('genres:all_genres')
    else:
        form = GenreForm()
    return render(request, 'genre_create.html', {'form': form})
def genres_detail(request, id):
    genre = Genres.objects.get(id=id)
    books = Book.objects.filter(genre_id=id)
    return render(request, 'book_list.html', {'genre': genre, 'books': books})
    