from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('topico/<int:id>/', views.topico_detail, name='topico_detail'),
    path('registrar/', views.registrar, name='registrar'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/<str:username>/', views.perfil_view, name='perfil_publico'),
    path('perfil/', views.perfil_view, name='perfil'), #atalho para 'meu perfil'
    path('topico/criar/', views.criar_topico, name='criar_topico'),
    
]