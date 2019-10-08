from django.db import models
from registers.models import Registers, RegistersAddress

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

    @staticmethod
    def get_address_from_pk(pk):
        list_codes = pk.split('.')
        return list_codes[0], list_codes[1]

    @staticmethod
    def get_orgin_data(user_pk):
        register = Registers.objects.filter(fk_user_id=user_pk)
        if not register:
            return {'status': 401, 'message': 'Invalid credentials (registers)!'}
        if len(register) > 0:
            register = register[0]
        address = RegistersAddress.objects.filter(fk_registers_id=register.pk_registers)
        address_default = address.filter(flag_default=True)
        if address_default:
            if len(address_default) > 0:
                address = address_default[0]
            country_origin, state_origin = Customers.get_address_from_pk(address_default.fk_cities_id)
            address = address_default
        elif address:
            if len(address) > 0:
                address = address[0]
            country_origin, state_origin = Customers.get_address_from_pk(address.fk_cities_id)
        else:
            return {'status': 401, 'message': 'Invalid credentials (Origin)!'}
        customer = Customers.objects.filter(fk_registers_id=register.pk_registers)
        if not customer:
            return {'status': 401, 'message': 'Invalid credentials (customers)!'}
        if len(customer) > 0:
            customer = customer[0]
        if customer.flag_block:
            return {'status': 401, 'message': 'User blocked!'}
        return {
            'country_origin': country_origin,
            'state_origin': state_origin,
            'from_user': register.name_register + ' - ' + address.country + '/' + address.state
        }
