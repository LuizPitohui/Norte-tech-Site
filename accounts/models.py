from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    
    # IMPORTANTE: null=True, blank=True permitem que o perfil seja criado vazio inicialmente
    full_name = models.CharField("Nome Completo", max_length=150, null=True, blank=True)
    cpf = models.CharField("CPF", max_length=14, unique=True, null=True, blank=True, validators=[
        RegexValidator(regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', message="CPF deve estar no formato 000.000.000-00")
    ])
    birth_date = models.DateField("Data de Nascimento", null=True, blank=True) # <--- O erro estava aqui
    phone = models.CharField("Celular/WhatsApp", max_length=20, null=True, blank=True)
    photo = models.ImageField("Foto de Perfil", upload_to="candidates/photos/", blank=True, null=True)
    
    # Endereço
    cep = models.CharField("CEP", max_length=9, null=True, blank=True)
    address = models.CharField("Endereço Completo", max_length=255, null=True, blank=True)
    city = models.CharField("Cidade", max_length=100, null=True, blank=True)
    state = models.CharField("Estado", max_length=2, null=True, blank=True)
    
    # Currículo Principal
    resume_file = models.FileField("Currículo em PDF", upload_to="candidates/resumes/", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.full_name}" if self.full_name else f"Perfil de {self.user.username}"

# ... (Mantenha as classes AcademicEducation, ProfessionalExperience e ExtraCourse como estavam) ...
class AcademicEducation(models.Model):
    LEVEL_CHOICES = [
        ('MEDIO', 'Ensino Médio'),
        ('TECNICO', 'Ensino Técnico'),
        ('SUPERIOR_CURSANDO', 'Ensino Superior (Cursando)'),
        ('SUPERIOR_COMPLETO', 'Ensino Superior (Completo)'),
        ('POS', 'Pós-Graduação/MBA'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')
    institution = models.CharField("Instituição", max_length=100)
    course = models.CharField("Curso", max_length=100)
    level = models.CharField("Nível", max_length=50, choices=LEVEL_CHOICES)
    start_date = models.DateField("Data de Início")
    end_date = models.DateField("Data de Conclusão", blank=True, null=True)
    
class ProfessionalExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField("Empresa", max_length=100)
    role = models.CharField("Cargo", max_length=100)
    start_date = models.DateField("Data de Início")
    end_date = models.DateField("Data de Saída", blank=True, null=True)
    description = models.TextField("Principais Atividades", blank=True)

class ExtraCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='extra_courses')
    name = models.CharField("Nome do Curso", max_length=150)
    institution = models.CharField("Instituição", max_length=100)
    hours = models.IntegerField("Carga Horária (horas)")
    completion_year = models.IntegerField("Ano de Conclusão")