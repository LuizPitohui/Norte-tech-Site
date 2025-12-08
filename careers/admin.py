from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe # Importação essencial para corrigir o erro
from django.contrib.auth.models import User
from .models import JobOpportunity, Candidate, DocumentType, CandidateDocument

# 1. Catálogo de Documentos (Ex: RG, CNH)
@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

# 2. Vagas
@admin.register(JobOpportunity)
class JobOpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'location', 'is_active', 'created_at')
    list_filter = ('department', 'is_active', 'location')
    search_fields = ('title', 'description')

# 3. Configuração da Tabela de Documentos (Inline)
class CandidateDocumentInline(admin.TabularInline):
    """
    Permite ao RH adicionar solicitações de documentos dentro da tela do candidato.
    """
    model = CandidateDocument
    extra = 1 # Mostra uma linha em branco para adicionar rápido
    fields = ('doc_type', 'file', 'status', 'rejection_reason')
    # O arquivo é readonly se quiser forçar o upload pelo usuário, 
    # mas deixei editável caso o RH receba por email e queira subir manualmente.

# 4. Gestão de Candidatos (O Painel Principal)
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    # Colunas da Lista
    list_display = ('name', 'job_display', 'status', 'sent_at', 'docs_status', 'download_resume')
    list_filter = ('status', 'job', 'sent_at')
    search_fields = ('name', 'email', 'hr_notes')
    list_editable = ('status',)
    
    # Injeta a tabela de documentos dentro do candidato
    inlines = [CandidateDocumentInline]
    
    # Organização Visual do Formulário
    fieldsets = (
        ('Informações da Candidatura', {
            'fields': ('job', 'name', 'email', 'phone', 'sent_at', 'resume_file')
        }),
        ('Currículo Interno (Dados do Perfil)', {
            'description': 'Estes dados são puxados automaticamente do perfil atual do usuário.',
            'fields': ('ver_formacao', 'ver_experiencia', 'ver_cursos')
        }),
        ('Área do RH (Gestão)', {
            'fields': ('status', 'hr_notes'),
            'classes': ('collapse',), # Começa fechado
        }),
    )
    
    # Campos calculados (HTML)
    readonly_fields = ('sent_at', 'ver_formacao', 'ver_experiencia', 'ver_cursos', 'docs_status')

    # --- Métodos Auxiliares ---

    def job_display(self, obj):
        return obj.job.title if obj.job else "Banco de Talentos"
    job_display.short_description = "Vaga"

    def download_resume(self, obj):
        if obj.resume_file:
            # Botão verde para baixar PDF
            return format_html("<a href='{}' target='_blank' style='background:#28a745; color:white; padding:4px 8px; border-radius:4px; text-decoration:none;'>Baixar PDF</a>", obj.resume_file.url)
        return "-"
    download_resume.short_description = "Arquivo"

    def docs_status(self, obj):
        """Mostra na lista se há documentos pendentes"""
        total = obj.documents.count()
        pendentes = obj.documents.filter(status='PENDENTE').count()
        rejeitados = obj.documents.filter(status='REJEITADO').count()
        
        if total == 0: 
            return "-"
        if rejeitados > 0:
            return format_html(f"<span style='color:red; font-weight:bold;'>{rejeitados} Rejeitado(s)</span>")
        if pendentes > 0: 
            return format_html(f"<span style='color:orange; font-weight:bold;'>{pendentes} Pendente(s)</span>")
        
        return format_html("<span style='color:green; font-weight:bold;'>✔ Tudo Certo</span>")
    docs_status.short_description = "Docs"

    # --- Renderização do Currículo Interno (Com mark_safe) ---

    def _get_user(self, obj):
        return User.objects.filter(email=obj.email).first()

    def ver_formacao(self, obj):
        user = self._get_user(obj)
        if not user: return "Usuário não encontrado."
        
        html = "<table style='width:100%; border-collapse: collapse; border: 1px solid #eee;'>"
        html += "<tr style='background:#f8f9fa; text-align:left;'><th style='padding:5px;'>Curso</th><th>Instituição</th><th>Nível</th><th>Conclusão</th></tr>"
        
        for item in user.educations.all():
            fim = item.end_date.strftime('%Y') if item.end_date else "Cursando"
            html += f"<tr style='border-top:1px solid #eee;'><td style='padding:5px;'>{item.course}</td><td>{item.institution}</td><td>{item.get_level_display()}</td><td>{fim}</td></tr>"
        
        html += "</table>"
        return mark_safe(html) # <--- O ERRO ESTAVA AQUI (Corrigido)
    ver_formacao.short_description = "Formação Acadêmica"

    def ver_experiencia(self, obj):
        user = self._get_user(obj)
        if not user: return "-"
        
        html = "<ul style='margin:0; padding-left:20px;'>"
        for item in user.experiences.all():
            fim = item.end_date.strftime('%m/%Y') if item.end_date else "Atual"
            inicio = item.start_date.strftime('%m/%Y')
            html += f"<li style='margin-bottom:10px;'><strong>{item.role}</strong> na <em>{item.company}</em> <small style='color:#666;'>({inicio} - {fim})</small><br><span style='font-style:italic; font-size:0.9em;'>{item.description}</span></li>"
        html += "</ul>"
        return mark_safe(html)
    ver_experiencia.short_description = "Experiência Profissional"

    def ver_cursos(self, obj):
        user = self._get_user(obj)
        if not user: return "-"
        
        html = "<ul style='margin:0; padding-left:20px;'>"
        for item in user.extra_courses.all():
            html += f"<li><strong>{item.name}</strong> - {item.institution} ({item.hours}h) em {item.completion_year}</li>"
        html += "</ul>"
        return mark_safe(html)
    ver_cursos.short_description = "Cursos Extras"