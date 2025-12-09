from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from services.models import Service
# Adicione 'Noticia' na importação abaixo
from .models import Certification, HomeVideo, OperatingBase, Noticia, CanalContato

def home(request):
    # Lógica do Formulário de Contato (Mantida)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            name=name, email=email, phone=phone, 
            subject=subject, message=message
        )
        messages.success(request, 'Mensagem enviada! Entraremos em contato.')
        return redirect('home')

    # --- LÓGICA DE EXIBIÇÃO ---
    
    # 1. Vídeo Hero (Destaque)
    video = HomeVideo.objects.filter(is_active=True).first()
    
    # 2. Notícias (Meio - Pegar as 4 últimas)
    noticias = Noticia.objects.all()[:4] 

    # (Opcional) Se quiser manter serviços e certificações abaixo das notícias, mantenha essas linhas:
    services = Service.objects.filter(is_active=True)[:6]
    certifications = Certification.objects.all()
    
    return render(request, 'home.html', {
        'video': video,
        'noticias': noticias,
        # Opcionais se for usar no resto da página
        'services': services, 
        'certifications': certifications,
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

def noticia_detail(request, slug):
    noticia = get_object_or_404(Noticia, slug=slug)
    return render(request, 'noticia_detail.html', {'noticia': noticia})

def todas_noticias(request):
    # Busca todas as notícias ordenadas da mais recente para a antiga
    noticias = Noticia.objects.all()
    return render(request, 'todas_noticias.html', {'noticias': noticias})

def contato(request):
    # Lógica de Exibição (Apenas busca os canais para mostrar)
    canais = CanalContato.objects.all()
    
    return render(request, 'contact.html', {
        'canais': canais
    })

def privacidade(request):
    return render(request, 'privacidade.html')