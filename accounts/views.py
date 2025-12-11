from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import CandidateProfile
from .forms import UserRegisterForm, CandidateProfileForm, EducationForm, ExperienceForm, CourseForm
from careers.models import Candidate

@login_required
def register(request):
    """
    Registra um novo usuário e cria seu perfil de candidato simultaneamente.
    """
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = CandidateProfileForm(request.POST, request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    # 1. Cria o Usuário
                    user = user_form.save()
                    
                    # 2. Cria o Perfil ligado ao Usuário
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.save()
                    
                    # 3. Loga o usuário e redireciona
                    login(request, user)
                    messages.success(request, 'Cadastro realizado com sucesso! Bem-vindo à Norte Tech.')
                    return redirect('profile')
                    
            except Exception as e:
                messages.error(request, f'Erro ao salvar os dados: {e}')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário abaixo.')
    else:
        user_form = UserRegisterForm()
        profile_form = CandidateProfileForm()

    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required # <--- Adicione esta linha!
def profile_view(request):
    """
    Dashboard do Candidato: Perfil + Histórico de Vagas.
    Protegido: Só usuários logados acessam.
    """
    # Agora o request.user sempre será um usuário real, nunca Anônimo
    profile, created = CandidateProfile.objects.get_or_create(user=request.user)
    
    # ... (o resto da função continua igual) ...
    my_applications = Candidate.objects.filter(email=request.user.email).order_by('-sent_at')

    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seus dados foram atualizados com sucesso!')
            return redirect('profile')
        else:
            print("❌ ERRO DE VALIDAÇÃO DO FORMULÁRIO:")
            print(form.errors)
            messages.error(request, 'Erro ao atualizar. Verifique os campos em vermelho abaixo.')
    else:
        form = CandidateProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': profile,
        'my_applications': my_applications
    })
# --- Views de Formação Acadêmica ---
@login_required
def add_education(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user
            education.save()
            messages.success(request, 'Formação adicionada!')
            return redirect('profile')
    else:
        form = EducationForm()
    return render(request, 'accounts/form_generic.html', {'form': form, 'title': 'Adicionar Formação'})

@login_required
def delete_education(request, pk):
    # Garante que só o dono pode deletar
    education = AcademicEducation.objects.get(pk=pk, user=request.user)
    education.delete()
    messages.success(request, 'Formação removida.')
    return redirect('profile')

# --- Views de Experiência ---
@login_required
def add_experience(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()
            messages.success(request, 'Experiência adicionada!')
            return redirect('profile')
    else:
        form = ExperienceForm()
    return render(request, 'accounts/form_generic.html', {'form': form, 'title': 'Adicionar Experiência'})

@login_required
def delete_experience(request, pk):
    experience = ProfessionalExperience.objects.get(pk=pk, user=request.user)
    experience.delete()
    messages.success(request, 'Experiência removida.')
    return redirect('profile')

# --- Views de Cursos ---
@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            messages.success(request, 'Curso adicionado!')
            return redirect('profile')
    else:
        form = CourseForm()
    return render(request, 'accounts/form_generic.html', {'form': form, 'title': 'Adicionar Curso'})

@login_required
def delete_course(request, pk):
    course = ExtraCourse.objects.get(pk=pk, user=request.user)
    course.delete()
    messages.success(request, 'Curso removido.')
    return redirect('profile')