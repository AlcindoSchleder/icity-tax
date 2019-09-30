from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from localization.models import Cities

# Create your models here.


class Categories(models.Model):
    TYPE_CATEGORIES_CHOICES = [
        (1, 'Administrador'),
        (2, 'Cliente'),
        (3, 'Consumidor'),
        (4, 'Fornecedor'),
        (5, 'Funcionário'),
    ]
    pk_categories = models.AutoField(primary_key=True, verbose_name='Código')
    name_cat = models.CharField(max_length=50, verbose_name='Descrição')
    flag_tcat = models.SmallIntegerField(choices=TYPE_CATEGORIES_CHOICES, default=2, verbose_name='Tipo de Categoria')
    flag_repr = models.BooleanField(default=False, verbose_name='Representante')

    class Meta:
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name_cat


class Registers(models.Model):
    TYPE_REGISTERS_CHOICES = [
        (1, 'Pessoa Física'),
        (2, 'Pessoa Jurídica')
    ]

    pk_registers = models.AutoField(primary_key=True, verbose_name='Código')
    fk_categories = models.ManyToManyField(
        Categories,
        related_name="categories",
        through='RegistersCategories',
        verbose_name='Categorias',
        help_text=(
            'Selecione as categorias a qual este usuário pertence. '
            'Elas são criadas sempre como ativas, posteriormente pode-se '
            'alterar o campo "ativo" no menu "Categorias do Usuário".'
        )
    )
    fk_user = models.ForeignKey(User, verbose_name='Login do Usuário', on_delete=models.PROTECT)
    flag_treg = models.SmallIntegerField(choices=TYPE_REGISTERS_CHOICES, verbose_name='Tipo')
    main_doc = models.CharField(max_length=20, unique=True, verbose_name='Documento de Identificação')
    secondary_doc = models.CharField(max_length=30, verbose_name='Outro Documento')
    first_name = models.CharField(max_length=50, verbose_name='Primeiro Nome')
    last_name = models.CharField(max_length=50, verbose_name='Sobrenome')
    alias_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nome Fantasia')
    enterprise_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='Nome da Empresa')
    insert_date = models.DateTimeField(auto_now_add=True, verbose_name='Data do Cadastro')
    kc_registers_address = models.SmallIntegerField(default=0, verbose_name='KeyControl RegistersAddresses')

    class Meta:
        verbose_name_plural = 'Usuários'

    @property
    def name_register(self):
        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        if self.alias_name:
            return self.alias_name
        else:
            return self.enterprise_name

    def __str__(self):
        return self.name_register


class RegistersCategories(models.Model):
    fk_categories = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Categoria')
    fk_registers = models.ForeignKey(Registers, on_delete=models.CASCADE, verbose_name='Pessoa/Empresa')
    flag_active = models.BooleanField(default=True, verbose_name='Ativo')
    insert_date = models.DateTimeField(auto_now_add=True, verbose_name='Data de inclusão')

    class Meta:
        verbose_name_plural = 'Categorias do Usuário'

    def __str__(self):
        return self.fk_categories.name_cat + ' - ' + self.fk_registers.name_register


class RegistersAddress(models.Model):
    TYPE_ADDRESS_CHOICES = [
        (1, 'Endereço Residencial'),
        (2, 'Endereço Comercial'),
        (3, 'Endereço de Cobrança'),
        (4, 'Endereço de Entrega'),
    ]
    pk_registers_address = models.IntegerField(primary_key=True, verbose_name='Código')
    fk_registers = models.ForeignKey(Registers, verbose_name='Usuário', on_delete=models.CASCADE)
    fk_cities = models.ForeignKey(Cities, verbose_name='Cidade', on_delete=models.PROTECT)
    flag_taddr = models.SmallIntegerField(choices=TYPE_ADDRESS_CHOICES, default=1, verbose_name='Typo')
    flag_default = models.BooleanField(default=False, verbose_name='Default')
    address = models.CharField(max_length=100, verbose_name='Endereço')
    number = models.IntegerField(verbose_name='Número')
    complement = models.CharField(max_length=100, null=True, blank=True, verbose_name='Complemento')
    quarter = models.CharField(max_length=50, verbose_name='Bairro')
    zip_code = models.CharField(max_length=15, verbose_name='C.E.P.')

    class Meta:
        verbose_name_plural = 'Endereços'
        indexes = [
            models.Index(fields=[
                'fk_cities',
                'zip_code'
            ], name='localization_idx'),
        ]

    @property
    def country(self):
        return self.fk_cities.country

    @property
    def state(self):
        return self.fk_cities.state

    @property
    def city(self):
        return self.fk_cities.name_city

    def __str__(self):
        return self.address + ', ' + str(self.number) + ' - ' + self.city + ' - ' + self.province + ' / ' + self.country


@receiver(pre_save, sender=RegistersAddress, dispatch_uid='before_save_registers_address')
def before_save_registers_address(instance, **kwargs):
    created = instance._state.adding
    if not created: return
    pk = str(instance.fk_registers_id) + str(instance.flag_taddr)
    instance.pk_registers_address = int(pk)
