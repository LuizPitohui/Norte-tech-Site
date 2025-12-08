from django.db import models
from django.core.exceptions import ValidationError

class CompanySettings(models.Model):
    """
    Singleton para gerenciar informações gerais do site (Rodapé, Contatos, Links).
    Baseado nas informações institucionais do PDF.
    """
    site_title = models.CharField("Título do Site", max_length=100, default="Norte Tech - Serviços em Energia")
    
    # Institucional
    mission = models.TextField("Missão", default="Garantir a satisfação de nossos clientes...", help_text="Texto da página 2 do Portfólio")
    vision = models.TextField("Visão", default="Ser reconhecida como a melhor prestadora...", help_text="Texto da página 2 do Portfólio")
    values = models.TextField("Valores", default="Valorização e respeito à vida; Segurança...", help_text="Texto da página 2 do Portfólio")
    
    # Contato (Baseado na página 9 e 42 do PDF)
    phone = models.CharField("Telefone Principal", max_length=20, blank=True)
    email_contact = models.EmailField("E-mail Comercial", default="comercial@nortetech.net")
    address = models.TextField("Endereço Matriz", default="Av. Torquato Tapajós, 12363 - Tarumã Açu - Manaus - AM")
    
    # Redes Sociais (Links fornecidos)
    instagram = models.URLField("Instagram", blank=True, help_text="https://www.instagram.com/nortetech.oficial/")
    linkedin = models.URLField("LinkedIn", blank=True, help_text="https://br.linkedin.com/company/norte-tech")
    youtube = models.URLField("YouTube", blank=True, help_text="https://www.youtube.com/@EmpresaNorteTech")
    facebook = models.URLField("Facebook", blank=True, help_text="https://www.facebook.com/NorteTechNT")
    
    class Meta:
        verbose_name = "Configuração da Empresa"
        verbose_name_plural = "Configurações da Empresa"

    def __str__(self):
        return "Configurações Gerais"

    def save(self, *args, **kwargs):
        # Garante que só exista 1 registro de configuração no banco
        if not self.pk and CompanySettings.objects.exists():
            raise ValidationError('Só é permitido ter uma configuração global.')
        return super(CompanySettings, self).save(*args, **kwargs)


class Certification(models.Model):
    """
    Para exibir os selos ISO 9001, 14001, 45001 e GPTW.
    """
    name = models.CharField("Nome do Certificado", max_length=100)
    image = models.ImageField("Imagem do Selo", upload_to="certifications/")
    order = models.IntegerField("Ordem de Exibição", default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Certificação"
        verbose_name_plural = "Certificações"

    def __str__(self):
        return self.name


class HomeVideo(models.Model):
    """
    Player de vídeo institucional para o topo da Home.
    Substitui o antigo HomeBanner.
    """
    title = models.CharField("Título de Identificação", max_length=100, help_text="Apenas para controle interno (ex: Vídeo Institucional 2025)")
    video_file = models.FileField("Arquivo de Vídeo (MP4)", upload_to="videos_home/")
    
    is_active = models.BooleanField("Ativo no Site?", default=True, help_text="Se marcar este, os outros vídeos serão desativados automaticamente.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Vídeo da Home"
        verbose_name_plural = "Vídeos da Home"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Lógica exclusiva: Se este vídeo for ativado, desativa todos os outros
        if self.is_active:
            HomeVideo.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super(HomeVideo, self).save(*args, **kwargs)


class ContactMessage(models.Model):
    """
    Salva as mensagens enviadas pelo formulário de contato do site.
    """
    name = models.CharField("Nome", max_length=100)
    email = models.EmailField("E-mail")
    phone = models.CharField("Telefone", max_length=20, blank=True)
    subject = models.CharField("Assunto", max_length=100)
    message = models.TextField("Mensagem")
    
    created_at = models.DateTimeField("Enviado em", auto_now_add=True)
    is_read = models.BooleanField("Lido?", default=False)

    class Meta:
        verbose_name = "Mensagem de Contato"
        verbose_name_plural = "Mensagens de Contato"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
class OperatingBase(models.Model):
    name = models.CharField("Nome da Base", max_length=100, help_text="Ex: Base Ponta Negra")
    address = models.CharField("Endereço", max_length=255, help_text="Ex: Av. Coronel Teixeira, S/N")
    city = models.CharField("Cidade/Estado", max_length=100, default="Manaus - AM")
    phone = models.CharField("Telefone", max_length=20, blank=True)
    image = models.ImageField("Foto da Base", upload_to="bases/", blank=True, null=True)
    map_link = models.URLField("Link do Google Maps", blank=True, help_text="Link para o botão 'Ver no Mapa'")
    
    order = models.IntegerField("Ordem de Exibição", default=0)

    class Meta:
        verbose_name = "Base Operacional"
        verbose_name_plural = "Bases Operacionais"
        ordering = ['order']

    def __str__(self):
        return self.name
    
