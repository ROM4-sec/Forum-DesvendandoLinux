from django.contrib import admin
from .models import Categoria, Topico, Resposta

# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug') #o que vai aparecer na lista
    prepopulated_fields = {'slug': ('nome',)} #Preenche o slug automaticamente enquanto você digita o nome

@admin.register(Topico)
class TopicoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'autor', 'data_criacao') #as colunas da tabela
    list_filter = ('categoria', 'data_criacao') #barra lateral dos filtros
    search_fields = ('titulo', 'conteudo') #barra de busca no topo
    raw_id_fields = ('autor',)
    
@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    list_display = ('topico', 'autor', 'data_criacao')
    list_filter = ('data_criacao',)
