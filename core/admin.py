from django.contrib import admin
# Adicionei 'CompanySettings' na lista de imports abaixo para corrigir o próximo erro
from .models import CompanySettings, Certification, HomeVideo, OperatingBase, Noticia, CanalContato
class CompanySettingsAdmin(admin.ModelAdmin):
    """
    Configuração Global: Impede que o usuário delete a configuração principal
    para não quebrar o site.
    """
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        # Remove o botão "Adicionar" se já existir uma configuração salva
        return not CompanySettings.objects.exists()


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)  # Permite reordenar os selos direto na lista
    ordering = ('order',)


@admin.register(HomeVideo)
class HomeVideoAdmin(admin.ModelAdmin):
    """
    Gestão do Player de Vídeo da Home.
    """
    list_display = ('title', 'is_active', 'created_at')
    list_editable = ('is_active',) # Permite ativar/desativar rápido
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    
    # Dica: Como a lógica do Model já desativa os outros vídeos ao ativar um novo,
    # o admin reflete isso automaticamente.

@admin.register(OperatingBase)
class OperatingBaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'phone', 'order')
    list_editable = ('order',)

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_criacao')
    search_fields = ('titulo', 'resumo')
    # Isso faz a mágica: cria o slug baseado no título automaticamente
    prepopulated_fields = {"slug": ("titulo",)}

@admin.register(CanalContato)
class CanalContatoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'conteudo', 'tipo', 'ordem')
    list_editable = ('ordem',)

