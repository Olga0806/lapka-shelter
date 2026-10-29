from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('', views.animal_list, name='animal_list'),
    path('animals/<int:pk>/', views.animal_detail, name='animal_detail'),
    path('animals/<int:pk>/apply/', views.application_create, name='application_create'),

    path('profile/', views.profile_view, name='profile'),

    path('animals/add/', views.animal_create, name='animal_create'),
    path('animals/<int:pk>/edit/', views.animal_update, name='animal_update'),
    path('animals/<int:pk>/delete/', views.animal_delete, name='animal_delete'),
    path('photos/<int:pk>/delete/', views.photo_delete, name='photo_delete'),
    path('applications/', views.application_list, name='application_list'),
    path('applications/<int:pk>/edit/', views.application_update, name='application_update'),
    path('applications/<int:pk>/delete/', views.application_delete, name='application_delete'),
]