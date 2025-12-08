from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import home, service_detail, about
from services.views import ServiceListAPI, service_list
from careers.views import careers_home, job_apply
from django.contrib.auth import views as auth_views
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('servicos/', service_list, name='services_list'),
    path('servico/<slug:slug>/', service_detail, name='service_detail'),
    path('api/v1/servicos/', ServiceListAPI.as_view(), name='api_services'),
    path('a-empresa/', about, name='about'),
    path('carreiras/', careers_home, name='careers_home'),
    # Rotas de Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', account_views.register, name='register'), # View customizada
    path('meu-perfil/', account_views.profile_view, name='profile'), # Painel do Candidato
    path('carreiras/aplicar/<int:job_id>/', job_apply, name='job_apply'), # <--- Nova rota

    # Currículo - Formação
    path('meu-perfil/formacao/adicionar/', account_views.add_education, name='add_education'),
    path('meu-perfil/formacao/deletar/<int:pk>/', account_views.delete_education, name='delete_education'),
    
    # Currículo - Experiência
    path('meu-perfil/experiencia/adicionar/', account_views.add_experience, name='add_experience'),
    path('meu-perfil/experiencia/deletar/<int:pk>/', account_views.delete_experience, name='delete_experience'),
    
    # Currículo - Cursos
    path('meu-perfil/curso/adicionar/', account_views.add_course, name='add_course'),
    path('meu-perfil/curso/deletar/<int:pk>/', account_views.delete_course, name='delete_course'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Redirecionamento após Login e Logout
LOGIN_REDIRECT_URL = 'profile'  # Nome da rota que definimos para /meu-perfil/
LOGOUT_REDIRECT_URL = 'home'    # Volta para a home ao sair
LOGIN_URL = 'login'