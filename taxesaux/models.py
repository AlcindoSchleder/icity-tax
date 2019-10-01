from django.db import models

# Create your models here.
from django.db.models import UniqueConstraint


class TypeTaxes(models.Model):
    TYPE_TAX_CHOICES = [
        (1, 'ICMS'),
        (2, 'ICMS_ST'),
        (3, 'IPI'),
        (4, 'ISS'),
        (5, 'ISENTO'),
        (6, 'Outros'),
    ]

    pk_type_taxes = models.AutoField(primary_key=True, verbose_name='Códugo: ')
    name_tax = models.CharField(max_length=50, verbose_name='Descrição: ')
    flag_tax = models.SmallIntegerField(choices=TYPE_TAX_CHOICES, default=1, verbose_name='Tipo de Imposto: ')

    class Meta:
        verbose_name_plural = "Tipos de Impostos"

    def __str__(self):
        return self.name_tax


class BaseUnits(models.Model):

    pk_baseunits = models.AutoField(primary_key=True, verbose_name='Código: ')
    name_unit = models.CharField(max_length=50, verbose_name='Descrição: ')
    unit_symbol = models.CharField(max_length=3, verbose_name='Unidade: ')
    repr_unit = models.SmallIntegerField(default=1, verbose_name='Representação: ')

    class Meta:
        verbose_name_plural = "Unidades"
        # constraints = [
        #     UniqueConstraint( fields=['unit_symbol'], name='baseunits_symbol_idx')
        # ]

    def __str__(self):
        return self.name_unit


class NcmCategories(models.Model):

    pk_ncmcategories = models.SmallIntegerField(primary_key=True, verbose_name='Códigp: ')
    name_ncmcat = models.CharField(max_length=200, verbose_name='Descrição: ')

    class Meta:
        verbose_name_plural = "Categoria NCM"

    def __str__(self):
        return self.name_ncmcat


class NcmCodes(models.Model):

    pk_ncmcodes = models.CharField(max_length=20, primary_key=True, verbose_name='Código: ')
    fk_ncmcategories = models.ForeignKey(NcmCategories, verbose_name='Categoria: ', on_delete=models.CASCADE)
    fk_baseunits = models.ForeignKey(BaseUnits, verbose_name='Unidade: ', on_delete=models.PROTECT)
    name_ncm = models.TextField(verbose_name='Descrição: ')
    flag_ipi = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Aliquota IPI: '
    )
    start_date = models.DateField(null=True, blank=True, verbose_name='Data de vigência Inicial: ')
    end_date = models.DateField(null=True, blank=True, verbose_name='Data de vigência Final: ')

    class Meta:
        verbose_name_plural = "Tabela NCM"

    def __str__(self):
        return self.name_ncm
