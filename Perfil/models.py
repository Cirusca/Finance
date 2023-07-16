from django.db import models
from datetime import datetime


class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)

    def __str__(self):
        return self.categoria
    
    def total_gasto(self):
        from extrato.models import Valores
        valores = Valores.objects.filter(categoria__id = self.id).filter(data__month=datetime.now().month).filter(tipo='S')
        
        total_valor =0
        for valor in valores:
            total_valor+= valor.valor #valor dentro das models
        
        return total_valor
        #TODO: TRANFORMAR ESSA FUNÇÃO EM UMA FUNÇÃO N UTILS
    def calcula_percentual_gasto_categoria(self):
        try: #ADICIONADO PARA EVITAR ZERO- ERROR DIVISION
            return int((self.total_gasto() * 100) / self.valor_planejamento)
        except:
            return 0
    #TODO: FAZER UMA BARRA TOTAL EM CIMA DAS BARRAS

class Conta(models.Model):
    banco_choices = (
        ('NU','Nubank'),
        ('CE', 'Caixa Economica')
    )
    tipo_choices = (
        ('PF', 'Pessoa fisica'),
        ('PJ', 'Pessoa jurídica')
    )
    apelido = models.CharField(max_length=20)
    banco = models.CharField(max_length=2, choices=banco_choices)
    tipo = models.CharField(max_length=2, choices=tipo_choices)
    valor = models.FloatField()
    icone = models.FileField(upload_to="icones")
    

    def __str__(self):
        return self.apelido
