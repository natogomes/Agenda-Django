from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse


# Create your views here.

# def index(request):
# return redirect('/agenda/')


def login_user(request):
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, 'Usuário ou senha inválido!')
    return redirect('/')


@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    evento = Evento.objects.filter(usuario=usuario,
                                   data_evento__gt=data_atual)
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)


@login_required(login_url='/login/')
def lista_expirado(request):
    usuario = request.user
    data_atual = datetime.now()
    evento = Evento.objects.filter(usuario=usuario,
                                   data_evento__lt=data_atual)
    dados = {'eventos': evento}
    return render(request, 'expirado.html', dados)


@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)


@login_required(login_url='/login/')
def submit_evento(request):
    try:
        if request.POST:
            titulo = request.POST.get('titulo')
            data_evento = request.POST.get('data_evento')
            descricao = request.POST.get('descricao')
            local = request.POST.get('local')
            usuario = request.user
            id_evento = request.POST.get('id_evento')

            if id_evento:
                evento = Evento.objects.get(id=id_evento)
                if evento.usuario == usuario:
                    evento.titulo = titulo
                    evento.data_evento = data_evento
                    evento.descricao = descricao
                    evento.local = local
                    evento.save()
                '''Evento.objects.filter(id=id_evento).update(titulo=titulo,
                                                           data_evento=data_evento,
                                                           descricao=descricao,
                                                           local=local)'''
            else:
                Evento.objects.create(titulo=titulo,
                                      data_evento=data_evento,
                                      descricao=descricao,
                                      local=local,
                                      usuario=usuario)
    except:
        return redirect('/')

    return redirect('/')


@login_required(login_url='/login/')
def submit_expirado(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        local = request.POST.get('local')
        usuario = request.user
        id_evento = request.POST.get('id_evento')

        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.data_evento = data_evento
                evento.descricao = descricao
                evento.local = local
                evento.save()
            '''Evento.objects.filter(id=id_evento).update(titulo=titulo,
                                                       data_evento=data_evento,
                                                       descricao=descricao,
                                                       local=local)'''
        else:
            Evento.objects.create(titulo=titulo,
                                  data_evento=data_evento,
                                  descricao=descricao,
                                  local=local,
                                  usuario=usuario)
    return redirect('/agenda/expirado/')


@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()

    return redirect('/')


@login_required(login_url='/login/')
def delete_expirado(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()

    return redirect('/agenda/expirado/')


def json_lista_evento(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo', 'descricao')
    return JsonResponse(list(evento), safe=False)
