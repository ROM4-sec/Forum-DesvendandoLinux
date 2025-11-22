from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    
    def __str__ (self):
        return self.nome
    
    class Meta:
        verbose_name_plural = "Categorias"
        
class Topico(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField(help_text="Use Markdown para formatar seu texto.")
    data_criacao = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    #Relações (chaves Estrangeiras)
    # Se a categoria for deletada, os tópicos somem (CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='topicos')
    
    #Se o usuário for deletado, o tópico continua mas sem autor ou deleta tudo?
    #vamos usar CASCADE (deleta tudo) para simplificar
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topico_criados')
    
    def __str__(self):
        return self.titulo
    
class Resposta(models.Model):
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    #relação com o tópico
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE, related_name='respostas')
    #relação com o autor
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Resposta de {self.autor} em {self.topico}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    AVATAR_CHOICES = [
        ('robo.png','Robô'),
        ('pinguin.png','Pinguin'),
        ('hacker.png','Hacker'),
        #adicionar mais imagens se necessário depois
    ]
    
    #campo de seleção (DROPDOWN)
    avatar = models.CharField(max_length=50, choices=AVATAR_CHOICES, default="pinguin.png")
    
    #Outros campos legais
    bio = models.TextField(max_length=500, blank=True, help_text="Fale um pouco sobre você.")
    distro = models.CharField(max_length=50, blank=True, help_text="Qual Distro Linux você esta usando no momento.")
    github = models.CharField(max_length=50, blank=True, help_text="Seu usuário no GitHub")
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        # Tenta salvar o perfil existente
        instance.profile.save()
    except Profile.DoesNotExist:
        # Se der erro porque não existe, cria um novo agora mesmo!
        Profile.objects.create(user=instance)