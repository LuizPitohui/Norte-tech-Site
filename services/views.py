from django.shortcuts import render
from rest_framework import generics
from .models import Service, ServiceCategory 
from .serializers import ServiceSerializer

class ServiceListAPI(generics.ListAPIView):
    """
    Endpoint para listar todos os serviços ativos em formato JSON.
    """
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer

def service_list(request):
    # Traz todas as categorias que tenham pelo menos um serviço ativo
    # O 'prefetch_related' otimiza o banco para não fazer 1 consulta por categoria
    categories = ServiceCategory.objects.prefetch_related('services').filter(services__is_active=True).distinct()
    
    return render(request, 'services_list.html', {
        'categories': categories
    })