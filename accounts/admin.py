from django.contrib import admin
from .models import CandidateProfile, AcademicEducation, ProfessionalExperience, ExtraCourse

class EducationInline(admin.TabularInline):
    model = AcademicEducation
    extra = 0

class ExperienceInline(admin.StackedInline):
    model = ProfessionalExperience
    extra = 0

class CourseInline(admin.TabularInline):
    model = ExtraCourse
    extra = 0

@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'cpf', 'city', 'phone')
    search_fields = ('full_name', 'cpf', 'email')
    # Isso permite ver cursos e experiencias dentro da tela do perfil do candidato no Admin
    # Nota: Como Education/Experience estão ligados ao USER e não ao Profile diretamente, 
    # precisaríamos de um ajuste fino aqui, mas vamos manter simples por enquanto.