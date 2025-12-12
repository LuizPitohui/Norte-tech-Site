from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models import Count , Q
from django.template.response import TemplateResponse
from .models import JobOpportunity, Candidate, DocumentType, CandidateDocument

class HRAdminSite(AdminSite):
    site_header = "Norte Tech - Admissão Digital"
    site_title = "Portal do RH"
    index_title = "Gestão de Processos Seletivos"
    index_template = 'admin/rh_dashboard.html'
    
    # Customizando a página inicial (Dashboard)
    def index(self, request, extra_context=None):
        # 1. Coletar Métricas Básicas
        total_vagas_abertas = JobOpportunity.objects.filter(is_active=True).count()
        total_candidatos = Candidate.objects.count()
        total_banco_talentos = Candidate.objects.filter(job__isnull=True).count() # Vaga vazia = Banco
        
        # 2. Funil de Seleção (Quantos em cada fase)
        # Usamos 'aggregate' para contar rapidinho
        funil = Candidate.objects.aggregate(
            novos=Count('id', filter=Q(status='NOVO')),
            entrevista=Count('id', filter=Q(status='ENTREVISTA')),
            admissao=Count('id', filter=Q(status__in=['AGUARDANDO_DOCS', 'DOCS_EM_ANALISE'])),
            contratados=Count('id', filter=Q(status='CONTRATADO')),
        )

        # 3. Vagas com mais candidatos (Top 5)
        top_vagas = JobOpportunity.objects.filter(is_active=True).annotate(
            num_cand=Count('candidates')
        ).order_by('-num_cand')[:5]

        # Passa esses dados para o template
        context = {
            'metricas': {
                'vagas_abertas': total_vagas_abertas,
                'total_candidatos': total_candidatos,
                'banco_talentos': total_banco_talentos,
                'funil': funil,
                'top_vagas': top_vagas,
            }
        }
        # Junta com o contexto padrão do admin (lista de apps)
        context.update(extra_context or {})
        return super().index(request, context)

# Instância do Painel de RH (Isolado do Admin principal)
rh_admin = HRAdminSite(name='rh_admin')

# --- CONFIGURAÇÃO DOS MODELS NO PAINEL DO RH ---

# 1. Catálogo de Documentos
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

# 2. Vagas
class JobOpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'candidatos_count', 'is_active', 'created_at')
    list_filter = ('department', 'is_active')
    search_fields = ('title',)
    
    def candidatos_count(self, obj):
        return obj.candidates.count()
    candidatos_count.short_description = "Candidatos"

# 3. Documentos Inline (Dentro do Candidato)
class CandidateDocumentInline(admin.TabularInline):
    model = CandidateDocument
    extra = 0
    fields = ('doc_type', 'file_link', 'status', 'rejection_reason')
    readonly_fields = ('file_link',)

    def file_link(self, obj):
        if obj.file:
            return format_html("<a href='{}' target='_blank'>Abrir Arquivo</a>", obj.file.url)
        return "-"
    file_link.short_description = "Arquivo"

# 4. Candidatos (Admissão)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'job_display', 'status', 'docs_status_rh', 'acoes_rapidas')
    list_filter = ('status', 'job', 'sent_at')
    search_fields = ('name', 'email', 'cpf')
    inlines = [CandidateDocumentInline]
    
    list_editable = ('status',)

    fieldsets = (
        ('Dados do Candidato', {
            'fields': ('job', 'name', 'email', 'phone', 'resume_file')
        }),
        ('Controle de Admissão', {
            'fields': ('status', 'hr_notes'),
            'description': 'Área exclusiva para gestão do processo seletivo.'
        }),
    )

    def job_display(self, obj):
        return obj.job.title if obj.job else "Banco de Talentos"
    job_display.short_description = "Vaga"

    def docs_status_rh(self, obj):
        total = obj.documents.count()
        pendentes = obj.documents.filter(status='PENDENTE').count()
        aprovados = obj.documents.filter(status='VALIDADO').count()
        
        if total == 0: return "-"
        
        cor = "orange"
        texto = f"{pendentes} Pendentes"
        
        if pendentes == 0 and total > 0:
            cor = "green"
            texto = "100% Validado"
        elif aprovados > 0:
            cor = "blue"
            texto = f"{aprovados}/{total} Ok"
            
        return format_html(f"<span style='color:{cor}; font-weight:bold;'>{texto}</span>")
    docs_status_rh.short_description = "Docs Admissão"

    def acoes_rapidas(self, obj):
        return format_html(
            "<a class='button' href='/carreiras/documentos/{}/' target='_blank'>Link de Envio</a>",
            obj.id
        )
    acoes_rapidas.short_description = "Link para o Candidato"

# --- REGISTRO NO PAINEL EXCLUSIVO DO RH ---
rh_admin.register(JobOpportunity, JobOpportunityAdmin)
rh_admin.register(Candidate, CandidateAdmin)
rh_admin.register(DocumentType, DocumentTypeAdmin)
# rh_admin.register(CandidateDocument) # Opcional, já aparece dentro do candidato