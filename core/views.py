from django.shortcuts import render
from .models import Categoria, Topico
from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Topico
from .forms import RespostaForm
from django.contrib.auth.forms import UserCreationForm
from .forms import RespostaForm, RegristrarUsuarioForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RespostaForm, ProfileForm#, RegistrarUsuarioForm

# Create your views here.

def home(request):
    #Busca todas as categarias
    categorias = Categoria.objects.all()
    
    #Busca os tópicos mais recentes (o '-' inverte a ordem, do mais novo pro mais velho)
    #O [:5] limita para pegar os 5 ultimos
    topicos_recentes = Topico.objects.order_by('-data_criacao')[:5]
    
    #Dicionário com os dados que vão para o HTML
    context = {
        'categorias': categorias,
        'topicos': topicos_recentes,
    }
    
    return render(request, 'core/home.html', context)

def topico_detail(request,id):
    #Busca o tópico pelo ID ou retorna um erro 404 se não achar
    topico = get_object_or_404(Topico, id=id)
    
    if request.method == 'POST':
        #Se alguém clicar em "enviar"
        form = RespostaForm(request.POST)
        if form.is_valid():
            resposta = form.save(commit=False)
            resposta.topico = topico #vincula a resposta a este tópico
            resposta.autor = request.user #vincula ao usuário logado (precisa estar logado)
            resposta.save()
            return redirect('topico_detail', id=topico.id)
    
    else:
        #Se for apenas um acesso normal (GET)
        form = RespostaForm()
        
    return render(request, 'core/topic_detail.html', {
        'topico':topico,
        'form': form
    })
    
def registrar(request):
    if request.method == 'POST':
        form = RegristrarUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') #manda pro login após cadastrar
    
    else: 
        form = RegristrarUsuarioForm()
        
    return render(request, 'registration/registrar.html', {'form': form})
        
@login_required        
def perfil_view(request, username=None):
    if username:
        user_obj = get_object_or_404(User, username=username)
    else:
        user_obj = request.user
    return render(request, 'core/profile.html', {'user_perfil':user_obj})        
        
@login_required
def editar_perfil(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
        
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('perfil')
        
    else:
        form = ProfileForm(instance=profile)
        
    return render(request, 'core/editar_perfil.html', {'form':form})