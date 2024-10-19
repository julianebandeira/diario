from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .models import Registro
from django.utils import timezone

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            senha = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=senha)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login realizado com sucesso!')
                return redirect('novo_registro')
            else:
                messages.error(request, 'E-mail ou senha inválidos.')
        else:
            messages.error(request, 'Formulário inválido. Por favor, tente novamente.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def registro_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('novo_registro')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro no campo {field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def novo_registro(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        conteudo = request.POST.get('conteudo')
        if titulo and conteudo:
            Registro.objects.create(usuario=request.user, titulo=titulo, conteudo=conteudo, data_criacao=timezone.now())
            messages.success(request, 'Registro salvo com sucesso!')
            return redirect('ler_registros')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')
    return render(request, 'registro.html')

@login_required
def ler_registros(request):
    registros = Registro.objects.filter(usuario=request.user).order_by('-data_criacao')
    return render(request, 'ler_registros.html', {'registros': registros})

@login_required
def editar_registro(request, registro_id):
    registro = get_object_or_404(Registro, id=registro_id, usuario=request.user)
    if request.method == 'POST':
        registro.titulo = request.POST.get('titulo')
        registro.conteudo = request.POST.get('conteudo')
        registro.save()
        messages.success(request, 'Registro atualizado com sucesso!')
        return redirect('ler_registros')
    return render(request, 'editar_registro.html', {'registro': registro})