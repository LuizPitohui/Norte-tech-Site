from django.db import models

class ServiceCategory(models.Model):
    """Categoria dos serviços (Ex: Manutenção, Projetos, Engenharia)"""
    name = models.CharField("Nome da Categoria", max_length=100)
    
    class Meta:
        verbose_name = "Categoria de Serviço"
        verbose_name_plural = "Categorias de Serviços"

    def __str__(self):
        return self.name

class Service(models.Model):
    """
    Serviços detalhados no portfólio.
    """
    # IMPORTANTE: related_name="services" é necessário para a View funcionar
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name="services")
    title = models.CharField("Título do Serviço", max_length=200)
    slug = models.SlugField(unique=True, help_text="URL amigável (ex: manutencao-subestacao)")
    
    # Conteúdo
    short_description = models.TextField("Resumo", max_length=300, help_text="Texto curto para o card na Home")
    full_description = models.TextField("Descrição Completa", help_text="Detalhes técnicos do serviço")
    
    # Mídia
    cover_image = models.ImageField("Imagem de Capa", upload_to="services/")
    icon_class = models.CharField("Ícone (FontAwesome/Bootstrap)", max_length=50, blank=True, help_text="Ex: bi-lightning-charge")
    
    # Status
    is_active = models.BooleanField("Ativo", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"

    def __str__(self):
        return self.title