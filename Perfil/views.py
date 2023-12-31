from django.shortcuts import render,redirect
from django.http import HttpResponse
from extrato.models import Valores
from extrato.views import novo_valor
from .models import Conta,Categoria
from django.contrib import messages
from django.contrib.messages import constants
from .utils import calcular_total,calcula_equilibio_financeiro
from datetime import datetime


# Create your views here.
def home(request):
    valores = Valores.objects.filter(data__month=datetime.now().month)
    entradas = valores.filter(tipo='E')
    saidas = valores.filter(tipo='S')

    total_entradas = calcular_total(entradas, 'valor')
    total_saidas = calcular_total(saidas, 'valor')
    total_livre = total_entradas - total_saidas
    
    contas = Conta.objects.all()
    total_contas = calcular_total(contas, 'valor')
    percentual_gastos_essenciais,percentual_gastos_nao_essenciais =  calcula_equilibio_financeiro()

    return render(request,'index.html', {'contas': contas, 
                                        'total_livre': total_livre,
                                        'total_contas' : total_contas, 
                                        'total_entradas': total_entradas, 
                                        'total_saidas': total_saidas,
                                        'percentual_gastos_essenciais': int(percentual_gastos_essenciais),
                                        'percentual_gastos_nao_essenciais': int(percentual_gastos_nao_essenciais)} )

def gerenciar(request): #enviar os dados para a UI/ Renderiza pro HTML
    contas = Conta.objects.all() #BUSCAR AS CONTAS
    categorias = Categoria.objects.all()#BUSCAR AS CATEGORIAS
    total_contas = calcular_total(contas, 'valor')
    return render(request,'gerenciar.html', {'contas': contas, 'total_contas' : total_contas, 'categorias': categorias,}) #variavel para o html

def cadastrar_banco(request): 
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    if len(apelido.strip()) == 0 or len(valor.strip()) == 0: #tratamento de erro

    #TO DO: MAIS VALIDAÇÕES
        messages.add_message(request, constants.ERROR, 'Campo não preenchido.')
        return redirect('/perfil/gerenciar/') 

    conta = Conta(
        apelido=apelido,
        banco = banco,
        tipo = tipo,
        valor = valor,
        icone = icone
    )
    conta.save()
    messages.add_message(request, constants.SUCCESS, 'Informações enviadas com sucesso.')
    return redirect('/perfil/gerenciar/')

def  deletar_banco(request, id):
    conta = Conta.objects.get(id = id) #buscar do banco
    valor = Valores.objects.filter(conta_id = id) #buscar do banco valores
    valor.delete()
    conta.delete()
    messages.add_message(request, constants.SUCCESS, 'Conta deletada com sucesso.')
    return redirect('/perfil/gerenciar/')

def cadastrar_categoria(request):
    nome_categoria = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))
    #TO DO: VALIDAÇÕES 

    categoria = Categoria(
        categoria = nome_categoria,
        essencial = essencial
    )
    if len(nome_categoria.split()) == 0:
        messages.add_message(request, constants.ERROR, 'Campo categoria não preenchido.')
        return redirect('/perfil/gerenciar/')
    categoria.save()
    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada.')
    return redirect('/perfil/gerenciar/')

def update_categoria(request,id):
    categoria = Categoria.objects.get(id=id)
    categoria.essencial = not categoria.essencial
    categoria.save()

    return redirect('/perfil/gerenciar/')

def dashboard(request): #cria as labels de graficos
    dados = {}
    categorias = Categoria.objects.all()
    for categoria in categorias:
        total = 0
        valores = Valores.objects.filter(categoria = categoria) 
        for v in valores:
            total += v.valor
        #TODO: BOTÕES DE IDA E VOLTA
        dados[categoria.categoria] = total
    return render(request, 'dashboard.html', {'labels':list(dados.keys()), 
                                              'values': list(dados.values())})