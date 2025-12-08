from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CandidateProfile, AcademicEducation, ProfessionalExperience, ExtraCourse
# 1. Formulário de Usuário (Login/Senha + Email)
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True, label="Primeiro Nome", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, label="Sobrenome", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name'] # Username será o login
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

# 2. Formulário de Perfil (CPF, Endereço, Arquivo)
class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        exclude = ['user', 'created_at', 'updated_at']
        
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome Completo Oficial'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(92) 90000-0000'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'resume_file': forms.FileInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CandidateProfileForm, self).__init__(*args, **kwargs)
        # Obriga o preenchimento de tudo no cadastro
        for field in self.fields:
            self.fields[field].required = True
        # Foto e Arquivo podem ser opcionais no início se você preferir, mas aqui deixei obrigatório
        self.fields['photo'].required = False

# Formulário de Formação Acadêmica
class EducationForm(forms.ModelForm):
    class Meta:
        model = AcademicEducation
        exclude = ['user']
        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

# Formulário de Experiência Profissional
class ExperienceForm(forms.ModelForm):
    class Meta:
        model = ProfessionalExperience
        exclude = ['user']
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# Formulário de Cursos Extras
class CourseForm(forms.ModelForm):
    class Meta:
        model = ExtraCourse
        exclude = ['user']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'completion_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }