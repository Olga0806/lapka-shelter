from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', views.RegisterView.as_view(), name='api_register'),
    path('profile/', views.ProfileView.as_view(), name='api_profile'),

    path('animals/', views.AnimalListView.as_view(), name='api_animals'),
    path('animals/<int:pk>/', views.AnimalDetailView.as_view(), name='api_animal_detail'),
    path('animals/<int:animal_pk>/apply/', views.ApplicationCreateView.as_view(), name='api_apply'),

    path('applications/', views.ApplicationListView.as_view(), name='api_applications'),
]