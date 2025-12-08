# core/context_processors.py
from .models import CompanySettings

def company_settings(request):
    """
    Disponibiliza as configurações da empresa (CompanySettings)
    para todos os templates do site automaticamente.
    """
    settings = CompanySettings.objects.first()
    return {'company_settings': settings}