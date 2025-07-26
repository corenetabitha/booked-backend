# /home/corene/project-backend/backend/api/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth.models import User
from .models import Book, Genre
from .serializers import BookSerializer, UserSerializer, GenreSerializer
from django.db.models import Q

# Genre ViewSet for CRUD operations on Genres
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_permissions(self):
        # Only admin users can create, update, or delete genres
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else: # list, retrieve
            self.permission_classes = [AllowAny] # Allow anyone to list/retrieve genres
        return [permission() for permission in self.permission_classes]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # REMOVED: The incorrect 'permission = [AllowAny]' line.
    # Permissions are now solely handled by the get_permissions method below.

    def get_permissions(self):
        # --- CORRECTED PERMISSIONS FOR BOOKVIEWSET ---
        if self.action in ['create']:
            # For development, allow anyone to create books.
            # You will change this back to IsAuthenticated or IsAdminUser when implementing full authentication.
            self.permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Only admin users can update or delete books.
            self.permission_classes = [IsAdminUser]
        else: # 'list' and 'retrieve' actions (GET requests)
            # Allow anyone to view the list of books and individual book details.
            self.permission_classes = [AllowAny]
        # --- END OF CORRECTION ---
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        queryset = Book.objects.all()
        search_term = self.request.query_params.get('search', None)
        genre_name = self.request.query_params.get('genre', None)
        availability = self.request.query_params.get('availability', None)
        sort_order = self.request.query_params.get('sort', 'latest')

        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) |
                Q(author__icontains=search_term)
            )
        if genre_name:
            queryset = queryset.filter(genre__name__iexact=genre_name)
        if availability == 'purchase':
            queryset = queryset.filter(is_available_for_purchase=True, stock_count__gt=0)
        elif availability == 'lending':
            queryset = queryset.filter(is_available_for_lending=True)

        if sort_order == 'latest':
            queryset = queryset.order_by('-date_added')
        elif sort_order == 'oldest':
            queryset = queryset.order_by('date_added')
        elif sort_order == 'price-asc':
            queryset = queryset.order_by('price')
        elif sort_order == 'price-desc':
            queryset = queryset.order_by('-price')

        return queryset

class UserRegisterLoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            is_admin = user.is_staff or user.is_superuser
            return Response({"message": "Login successful", "user": {"id": user.id, "username": user.username, "is_admin": is_admin}}, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)