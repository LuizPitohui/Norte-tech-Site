from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import JobOpportunity, Candidate, CandidateDocument
from accounts.models import CandidateProfile # Importando do outro app

def careers_home(request):
    """
    Lista as vagas abertas.
    """
    jobs = JobOpportunity.objects.filter(is_active=True)
    return render(request, 'careers_home.html', {'jobs': jobs})

@login_required
def job_apply(request, job_id):
    """
    Lógica para aplicar para uma vaga usando o perfil existente.
    """
    job = get_object_or_404(JobOpportunity, id=job_id, is_active=True)
    user = request.user
    
    # 1. Tenta pegar o perfil
    try:
        # Tenta acessar o perfil. Se não existir, vai gerar erro.
        if not hasattr(user, 'candidate_profile'):
            raise ObjectDoesNotExist
        profile = user.candidate_profile
    except ObjectDoesNotExist:
        messages.warning(request, "Seu perfil está incompleto. Preencha seus dados para se candidatar.")
        return redirect('profile')
    
    # 2. Verifica se tem currículo anexado
    if not profile.resume_file:
        messages.error(request, "Você precisa anexar seu Currículo (PDF) no menu 'Meu Perfil' antes de aplicar.")
        return redirect('profile')

    # 3. Verifica se já aplicou
    if Candidate.objects.filter(email=user.email, job=job).exists():
        messages.warning(request, f"Você já se candidatou para a vaga de {job.title}.")
        return redirect('careers_home')

    # 4. Salva a candidatura
    Candidate.objects.create(
        job=job,
        name=profile.full_name or user.username,
        email=user.email,
        phone=profile.phone or "Não informado",
        resume_file=profile.resume_file,
        message=f"Aplicação via perfil do usuário {user.username}"
    )
    
    messages.success(request, f"Sucesso! Sua candidatura para {job.title} foi enviada.")
    return redirect('careers_home')

@login_required
def onboarding_view(request, candidate_id):
    """
    Tela onde o candidato vê os documentos solicitados e faz upload.
    """
    # Segurança: Só acessa se o candidato for do usuário logado
    candidate = get_object_or_404(Candidate, id=candidate_id, email=request.user.email)
    
    documents = candidate.documents.all()

    if request.method == 'POST':
        # Identifica qual documento está sendo enviado pelo ID escondido no form
        doc_id = request.POST.get('doc_id')
        uploaded_file = request.FILES.get('file')
        
        if doc_id and uploaded_file:
            doc_request = get_object_or_404(CandidateDocument, id=doc_id, candidate=candidate)
            
            doc_request.file = uploaded_file
            doc_request.status = 'ENVIADO' # Muda status automaticamente
            doc_request.rejection_reason = '' # Limpa rejeição anterior se houver
            doc_request.save()
            
            messages.success(request, f"Arquivo para {doc_request.doc_type} enviado com sucesso!")
            return redirect('onboarding', candidate_id=candidate.id)
        else:
            messages.error(request, "Erro ao enviar arquivo.")

    return render(request, 'careers_onboarding.html', {
        'candidate': candidate,
        'documents': documents
    })