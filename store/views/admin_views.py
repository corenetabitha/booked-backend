
from django.http import JsonResponse
from store.utils.decorators import admin_required
from store.models import Book
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@admin_required
def add_book(request):
    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        title = data.get('title')
        author = data.get('author')
        price = data.get('price')
        description = data.get('description', '')
        published_at = data.get('published_at', None)

        book = Book.objects.create(
            title=title,
            author=author,
            price=price,
            description=description,
            published_at=published_at
        )

        return JsonResponse({
            'message': 'Book added successfully',
            'book': {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'price': str(book.price),
                'description': book.description,
                'published_at': str(book.published_at) if book.published_at else None,
            }
        }, status=201)

    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=400)
