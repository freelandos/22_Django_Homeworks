from django.shortcuts import render, redirect

from books.models import Book


def index(request):
    return redirect('books')


def books_view(request, pub_date=None):
    template = 'books/books_list.html'
    books = Book.objects.order_by('pub_date')
    prev_date, next_date = '', ''
    if pub_date:
        books = Book.objects.filter(pub_date=pub_date)
        prev_book = Book.objects.filter(pub_date__lt=pub_date).order_by('pub_date').last()
        if prev_book:
            prev_date = prev_book.pub_date
        next_book = Book.objects.filter(pub_date__gt=pub_date).order_by('pub_date').first()
        if next_book:
            next_date = next_book.pub_date
    context = {
        'books': books,
        'prev_date': prev_date,
        'next_date': next_date
    }
    return render(request, template, context)
