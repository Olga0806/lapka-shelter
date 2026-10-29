from rest_framework import serializers
from django.contrib.auth.models import User

from animals.models import Animal, AnimalPhoto, Application


class AnimalPhotoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = AnimalPhoto
        fields = ['id', 'image']


class AnimalSerializer(serializers.ModelSerializer):
    photos = AnimalPhotoSerializer(many=True, read_only=True)
    species_display = serializers.CharField(source='get_species_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = Animal
        fields = [
            'id', 'name', 'species', 'species_display',
            'breed', 'age', 'gender', 'gender_display',
            'description', 'photos', 'created_at',
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    animal_name = serializers.CharField(source='animal.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    housing_display = serializers.CharField(source='get_housing_display', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'animal', 'animal_name',
            'full_name', 'phone', 'age',
            'housing', 'housing_display',
            'family_size', 'other_animals', 'comment',
            'status', 'status_display', 'created_at',
        ]
        read_only_fields = ['animal', 'status', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'full_name', 'phone', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        user.first_name = validated_data['full_name']
        user.last_name = validated_data['phone']
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='first_name', read_only=True)
    phone = serializers.CharField(source='last_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'phone']