from django.db import models
from registers.models import Registers

# Create your models here.


class Customers(models.Model):
    fk_registers = models.OneToOneField(Registers, verbose_name='Usuário: ', on_delete=models.CASCADE)
    flag_cnsm = models.BooleanField(default=False, verbose_name='Consumidor Final')
    flag_block = models.BooleanField(default=False, verbose_name='Cliente Bloqueado')
    credit_limit = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Limite de Crédito: ')
    date_block = models.DateTimeField(null=True, blank=True, verbose_name='Data do Bloqueio: ')
    mot_block = models.TextField(null=True, blank=True, verbose_name='Motivo do Bloqueio: ')

    class Meta:
        verbose_name_plural = 'clientes'

    @property
    def name_customer(self):
        return self.fk_registers.name_register

    def __str__(self):
        return self.name_customer

