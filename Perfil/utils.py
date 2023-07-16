from extrato.models import Valores
from datetime import datetime
def calcular_total(obj, campo): #obj é categorias/contas
    total = 0
    for i in obj:
        total+= getattr(i,campo) # calculo um atributo
    return total

def calcula_equilibio_financeiro():
    gastos_essenciais = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=True)
    gastos_nao_essenciais = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=False)
    
    total_gastos_e = calcular_total(gastos_essenciais, 'valor')
    total_n_gastos_e = calcular_total(gastos_nao_essenciais, 'valor')
    total = total_n_gastos_e + total_gastos_e
    try:
        percentual_essen = (total_gastos_e*100)/total
        percentual_n_essen = (total_n_gastos_e*100)/total
        return percentual_essen, percentual_n_essen
    except:
        return 0,0


