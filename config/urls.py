from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# 1. ADICIONEI 'noticia_detail' NA IMPORTAÇÃO ABAIXO
from core.views import home, service_detail, about, noticia_detail, todas_noticias, contato, privacidade
from services.views import ServiceListAPI, service_list
from careers.views import careers_home, job_apply, onboarding_view, job_detail, candidate_history, talent_bank_view
from django.contrib.auth import views as auth_views
from accounts import views as account_views
from careers.admin_rh import rh_admin

urlpatterns = [
    path('admin/', admin.site.urls),
    # Painel Exclusivo RH (Admissão Digital)
    path('rh/', rh_admin.urls),
    path('', home, name='home'),
    
    # 2. NOVA ROTA DE NOTÍCIAS ADICIONADA AQUI:
    path('noticias/', todas_noticias, name='todas_noticias'),
    path('noticias/<slug:slug>/', noticia_detail, name='noticia_detail'),
    path('privacidade/', privacidade, name='privacidade'),
    path('servicos/', service_list, name='services_list'),
    path('servico/<slug:slug>/', service_detail, name='service_detail'),
    path('api/v1/servicos/', ServiceListAPI.as_view(), name='api_services'),
    path('a-empresa/', about, name='about'),
    path('carreiras/', careers_home, name='careers_home'),
    path('fale-conosco/', contato, name='contato_page'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', account_views.register, name='register'),
    path('meu-perfil/', account_views.profile_view, name='profile'),
    path('carreiras/aplicar/<int:job_id>/', job_apply, name='job_apply'),
    path('carreiras/vaga/<int:job_id>/', job_detail, name='job_detail'),
    path('carreiras/banco-de-talentos/aplicar/', job_apply, name='job_apply_bank'), # Reusa a view sem ID
    path('carreiras/banco-de-talentos/', talent_bank_view, name='talent_bank'),
    path('meu-perfil/historico/', candidate_history, name='candidate_history'),
    path('meu-perfil/formacao/adicionar/', account_views.add_education, name='add_education'),
    path('meu-perfil/formacao/deletar/<int:pk>/', account_views.delete_education, name='delete_education'),
    path('meu-perfil/experiencia/adicionar/', account_views.add_experience, name='add_experience'),
    path('meu-perfil/experiencia/deletar/<int:pk>/', account_views.delete_experience, name='delete_experience'),
    path('meu-perfil/curso/adicionar/', account_views.add_course, name='add_course'),
    path('meu-perfil/curso/deletar/<int:pk>/', account_views.delete_course, name='delete_course'),
    path('meu-perfil/historico/', candidate_history, name='candidate_history'),
    path('carreiras/documentos/<int:candidate_id>/', onboarding_view, name='onboarding'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Redirecionamento após Login e Logout
LOGIN_REDIRECT_URL = 'profile'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'