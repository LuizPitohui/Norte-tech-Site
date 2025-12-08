from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from services.models import Service
# AQUI ESTAVA O ERRO: Trocamos HomeBanner por HomeVideo
from .models import Certification, HomeVideo, ContactMessage, OperatingBase

def home(request):
    # Lógica do Formulário de Contato (POST)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Salva no banco
        ContactMessage.objects.create(
            name=name, email=email, phone=phone, 
            subject=subject, message=message
        )
        
        messages.success(request, 'Sua mensagem foi enviada com sucesso! Entraremos em contato em breve.')
        return redirect('home')

    # Lógica de Exibição (GET)
    services = Service.objects.filter(is_active=True)[:6]
    certifications = Certification.objects.all()
    
    # Pega o vídeo ativo (Substituindo a lógica do banner antigo)
    video = HomeVideo.objects.filter(is_active=True).first()
    
    return render(request, 'home.html', {
        'services': services,
        'certifications': certifications,
        'video': video # Passamos 'video' em vez de 'banner'
    })

def service_detail(request, slug):
    # Busca o serviço pelo slug ou retorna erro 404 se não achar
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    return render(request, 'service_detail.html', {
        'service': service
    })

def about(request):
    bases = OperatingBase.objects.all()
    # Podemos reutilizar as certificações aqui também se quiser
    certifications = Certification.objects.all()
    
    return render(request, 'about.html', {
        'bases': bases,
        'certifications': certifications
    })