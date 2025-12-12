from django.db import models

class JobOpportunity(models.Model):
    """
    Vagas disponíveis cadastradas pelo RH.
    """
    title = models.CharField("Título da Vaga", max_length=100)
    department = models.CharField("Departamento", max_length=100, choices=[
        ('OPERACIONAL', 'Operacional (Campo)'),
        ('ENGENHARIA', 'Engenharia'),
        ('ADMINISTRATIVO', 'Administrativo'),
        ('TECNOLOGIA', 'Tecnologia (TI)'),
        ('FROTA', 'Gestão de Frota'),
    ])
    location = models.CharField("Localização", max_length=100, default="Manaus - AM")
    description = models.TextField("Descrição da Vaga")
    requirements = models.TextField("Requisitos")
    benefits = models.TextField("Benefícios", blank=True)
    
    salary_range = models.CharField("Faixa Salarial", max_length=100, blank=True, help_text="Opcional")
    
    # --- NOVO CAMPO: Número de Vagas ---
    vacancies = models.PositiveIntegerField("Número de Vagas", default=1, help_text="Quantas posições estão abertas")
    
    is_active = models.BooleanField("Vaga Aberta?", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Vaga"
        verbose_name_plural = "Vagas Disponíveis"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.location})"


class Candidate(models.Model):
    """
    Candidatos que aplicaram para uma vaga específica ou banco de talentos.
    """
    # Vaga é opcional (null=True), pois ele pode mandar para "Banco de Talentos" geral
    job = models.ForeignKey(JobOpportunity, on_delete=models.SET_NULL, null=True, blank=True, related_name="candidates", verbose_name="Vaga Pretendida")
    
    name = models.CharField("Nome Completo", max_length=100)
    email = models.EmailField("E-mail")
    phone = models.CharField("Telefone/WhatsApp", max_length=20)
    
    resume_file = models.FileField("Currículo (PDF/DOC)", upload_to="resumes/%Y/%m/") # Organiza por ano/mês
    message = models.TextField("Mensagem/Apresentação", blank=True)
    
    # Controle do RH (Status Atualizados para Admissão Digital)
    STATUS_CHOICES = [
        ('NOVO', 'Novo Recebido'),
        ('ANALISE', 'Em Análise'),
        ('ENTREVISTA', 'Entrevista Agendada'),
        ('BANCO', 'Banco de Talentos'),
        ('REPROVADO', 'Reprovado'),
        # Novos Status de Admissão:
        ('AGUARDANDO_DOCS', 'Aprovado - Aguardando Documentos'),
        ('DOCS_EM_ANALISE', 'Documentos em Análise'),
        ('CONTRATADO', 'Contratado'),
    ]
    status = models.CharField("Status do Processo", max_length=20, choices=STATUS_CHOICES, default='NOVO')
    hr_notes = models.TextField("Anotações do RH", blank=True, help_text="Interno - Candidato não vê")
    
    # --- NOVOS CAMPOS: Termos e LGPD ---
    terms_accepted = models.BooleanField("Aceitou Termos/LGPD?", default=False)
    terms_accepted_at = models.DateTimeField("Data do Aceite", null=True, blank=True)
    
    sent_at = models.DateTimeField("Enviado em", auto_now_add=True)

    class Meta:
        verbose_name = "Candidato"
        verbose_name_plural = "Gestão de Candidatos"
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"
    
class DocumentType(models.Model):
    """Catálogo de tipos de documentos que a empresa pode pedir."""
    title = models.CharField("Nome do Documento", max_length=100, help_text="Ex: CNH, RG, Comprovante de Residência")
    description = models.TextField("Instruções", blank=True, help_text="Ex: Enviar frente e verso legível.")

    def __str__(self):
        return self.title

class CandidateDocument(models.Model):
    """Documentos solicitados a um candidato específico."""
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT, verbose_name="Tipo de Documento")
    
    # Arquivo enviado pelo usuário
    file = models.FileField("Arquivo Enviado", upload_to="candidate_docs/%Y/%m/", blank=True, null=True)
    
    # Controle de Status
    STATUS_CHOICES = [
        ('PENDENTE', 'Aguardando Envio'),
        ('ENVIADO', 'Em Análise pelo RH'),
        ('VALIDADO', 'Documento Aceito'),
        ('REJEITADO', 'Rejeitado (Reenviar)'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    rejection_reason = models.TextField("Motivo da Rejeição", blank=True, help_text="Preencher se rejeitar o documento")
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Documento do Candidato"
        verbose_name_plural = "Documentos Solicitados"

    def __str__(self):
        return f"{self.doc_type} - {self.candidate.name}"