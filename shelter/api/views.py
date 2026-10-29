from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from animals.models import Animal, Application
from .serializers import (
    AnimalSerializer,
    ApplicationSerializer,
    RegisterSerializer,
    UserSerializer,
)


class AnimalListView(generics.ListAPIView):
    """GET /api/animals/ — список животных (с фильтрами)."""
    serializer_class = AnimalSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Animal.objects.all()
        q = self.request.query_params.get('q', '').strip()
        species = self.request.query_params.get('species', '')

        if q:
            qs = qs.filter(name__icontains=q) | qs.filter(breed__icontains=q)
        if species:
            qs = qs.filter(species=species)
        return qs


class AnimalDetailView(generics.RetrieveAPIView):
    """GET /api/animals/<id>/ — карточка животного."""
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [permissions.AllowAny]


class RegisterView(APIView):
    """POST /api/register/ — регистрация клиента."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Регистрация успешна'}, status=201)
        return Response(serializer.errors, status=400)


class ProfileView(APIView):
    """GET /api/profile/ — профиль с заявками."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_data = UserSerializer(request.user).data
        apps = Application.objects.filter(user=request.user).select_related('animal')
        apps_data = ApplicationSerializer(apps, many=True).data
        return Response({
            'user': user_data,
            'applications': apps_data,
        })


class ApplicationCreateView(APIView):
    """POST /api/animals/<id>/apply/ — подать заявку на животное."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, animal_pk):
        animal = get_object_or_404(Animal, pk=animal_pk)

        existing = Application.objects.filter(
            user=request.user, animal=animal, status__in=['new', 'approved']
        ).first()
        if existing:
            return Response(
                {'error': 'У вас уже есть активная заявка на это животное'},
                status=400
            )

        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, animal=animal)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ApplicationListView(generics.ListAPIView):
    """GET /api/applications/ — заявки (только для кинолога)."""
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Application.objects.all().select_related('animal')