from django.db.models import Exists, OuterRef, Value, BooleanField
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required

from .models import Category, Book, Comment, BookLike
from .forms import BookForm, CommentForm


def home(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        if request.GET.get('q'):
            books = Book.objects.filter(
                booklike__user=request.user,
                published=True
            ).annotate(
                is_like=Value(True, output_field=BooleanField())
            )

        else:
            books = Book.objects.filter(published=True).annotate(
                is_like = Exists(
                    BookLike.objects.filter(
                        user=request.user,
                        book=OuterRef('pk')
                    )
                )
            )
    else:
        books = Book.objects.filter(published=True)
    context = {
        'categories': categories,
        'books': books,
        'title': "Kitoblar olami"
    }
    return render(request, 'main/index.html', context)


def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    categories = Category.objects.all()
    comments = Comment.objects.filter(book=book).order_by('-created')

    book.views += 1
    book.save()

    context = {
        'book': book,
        'categories': categories,
        'form': CommentForm(),
        'comments': comments
    }

    return render(request, 'main/detail.html', context)


def book_by_category(request, category_id):
    categories = Category.objects.all()
    category = Category.objects.get(id=category_id)
    books = Book.objects.filter(category=category)

    context = {
        'categories': categories,
        'books': books,
        'title': category.name
    }
    return render(request, 'main/index.html', context)


def add_book(request: HttpRequest):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = BookForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                book = form.save()
                return redirect('detail', book_id=book.pk)
        else:
            form = BookForm()
        context = {
            'form': form
        }
        return render(request, 'main/add_book.html', context)
    else:
        return redirect('home')


def update_book(request, book_id: int):
    book = Book.objects.get(id=book_id)

    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('detail', book_id=book.id)

    form = BookForm(instance=book)
    context = {
        'form': form
    }
    return render(request, 'main/add_book.html', context)


def delete_book(request, book_id: int):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('home')
    context = {
        'book': book
    }
    return render(request, 'main/confirm_delete.html', context)


# ----------------------start comment--------------------

@login_required(login_url='home')
def save_comment(request, book_id: int):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.book = book
            comment.user = request.user
            comment.save()
    return redirect('detail', book_id=book.pk)


@login_required(login_url='home')
def update_comment(request, book_id: int, comment_id: int):
    comment = Comment.objects.get(id=comment_id, book_id=book_id)
    context = {}
    if request.user == comment.user:
        if request.method == 'POST':
            form = CommentForm(data=request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('detail', book_id=book_id)
        context['form'] = CommentForm(instance=comment)
    return render(request, 'main/update_comment.html', context)


@login_required(login_url='home')
def delete_comment(request, comment_id: int):
    comment = Comment.objects.get(pk=comment_id)
    if comment.user == request.user or request.user.is_superuser:
        if request.method == 'POST':
            book_id = comment.book.pk
            comment.delete()
            return redirect('detail', book_id=book_id)
        return render(request, 'main/confirm_delete_comment.html', {'comment': comment})
    else: return redirect('home')

# ----------------------end comment----------------------

# ----------------------start like----------------------

@login_required(login_url='home')
def add_like_for_book(request, book_id: int):
    book_like, created = BookLike.objects.get_or_create(book_id=book_id, user=request.user)
    if not created:
        book_like.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

# ----------------------end like------------------------
