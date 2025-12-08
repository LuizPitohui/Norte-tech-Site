from rest_framework import serializers
from .models import Service, ServiceCategory

class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'title', 'slug', 'category_name', 'short_description', 'cover_image']