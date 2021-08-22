from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
# Create your models here.


class Evento(models.Model):
    titulo = models.CharField(max_length=100, blank=False, null=False)
    descricao = models.TextField(blank=True, null=True)
    data_evento = models.DateTimeField(verbose_name='Data do Evento')
    data_criacao = models.DateTimeField(auto_now=True, verbose_name='Data da criação')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    local = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'Evento'

    def __str__(self):
        return self.titulo

    def get_data_evento(self):
        return self.data_evento.strftime('%d/%m/%y - %H:%Mh')

    def get_data_criacao(self):
        return self.data_criacao.strftime('%d/%m/%y - %H:%Mh')

    def get_data_input_evento(self):
        return self.data_evento.strftime('%Y-%m-%dT%H:%M')

    def get_evento_atrasado(self):
        if self.data_evento < datetime.now():
            return True
        else:
            return False

    def get_evento_pre(self):
        if self.data_evento < datetime.now() + timedelta(hours=1):
            return True
        else:
            return False
