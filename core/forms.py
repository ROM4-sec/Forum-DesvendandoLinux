from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Resposta, Profile

class RespostaForm(forms.ModelForm):
    class Meta:
        model = Resposta
        fields = ['conteudo'] #Só queremos que o usuário digite o conteúdo
        widgets = {
            'conteudo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Digite sua resposta aqui...'
            }),
        }
        
class RegristrarUsuarioForm(UserCreationForm):
    #adicionamos o campo email explicitamente com validação
    email = forms.EmailField(required=True, label="Endereço de Email")
    
    class Meta: 
        model = User
        
        #definimos quais campos aparecem na ordem
        fields = ("username", "email")
        
    #Verificar se o email já existe no banco
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já esta cadastrado.")
        return email
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'distro','github']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'distro':forms.TextInput(attrs={'class': 'form-control'}),
            'github':forms.TextInput(attrs={'class': 'form-control'}),
            'avatar':forms.Select(attrs={'class': 'form-select'}),
        }