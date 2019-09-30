from django.db import models
from localization.models import Countries, States
from taxesaux.models import TypeTaxes, NcmCodes

# Create your models here.


class Taxes(models.Model):
    pk_taxes = models.CharField(max_length=15, primary_key=True, verbose_name='Código')
    fk_type_taxes = models.ForeignKey(
        TypeTaxes,
        default=1,
        verbose_name='Tipo de Imposto',
        on_delete=models.PROTECT
    )
    fk_countries_origin = models.ForeignKey(
        Countries,
        related_name='pk_countries_origin',
        related_query_name='countries_origin',
        verbose_name='País de Origem',
        default=55,
        on_delete=models.PROTECT
    )
    fk_states_origin = models.ForeignKey(
        States,
        verbose_name='Estado de Origem',
        related_name='pk_states_origin',
        related_query_name='states_origin',
        default='',
        on_delete=models.PROTECT
    )
    fk_countries_destiny = models.ForeignKey(
        Countries,
        related_name='pk_countries_destiny',
        related_query_name='countries_destiny',
        verbose_name='País de Destino',
        default=55,
        on_delete=models.PROTECT
    )
    fk_states_destiny = models.ForeignKey(
        States,
        related_name='pk_states_destiny',
        related_query_name='states_destiny',
        verbose_name='Estado de Destino',
        default='',
        on_delete=models.PROTECT
    )
    taxdef = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=True, verbose_name='Percentual: ')

    class Meta:
        verbose_name_plural = 'Impostos Default'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'fk_type_taxes',
                    'fk_countries_origin',
                    'fk_states_origin',
                    'fk_countries_destiny',
                    'fk_states_destiny',
                ],
                name='pk_taxes'
            )
        ]

    def __str__(self):
        return '%.2f' % self.taxdef


def before_save_taxes(instance, **kwargs):
    created = instance._state.adding
    if not created: return
    pk = str(instance.fk_type_taxes_id) + '.' + str(instance.fk_countries_origin_id) + '.' + \
         instance.fk_states_origin_id + '.' + str(instance.fk_countries_destiny_id) + '.' + \
         instance.fk_states_destiny_id
    instance.pk_taxes = pk


models.signals.pre_save.connect(before_save_taxes, sender=Taxes, dispatch_uid='before_save_taxes')


class NcmTaxes(models.Model):
    pk_ncmtaxes = models.AutoField(primary_key=True, verbose_name='Código')
    fk_taxes = models.ForeignKey(Taxes, verbose_name='Alíquota default', on_delete=models.CASCADE)
    fk_ncmcodes = models.ForeignKey(NcmCodes, verbose_name='NCM do Produto', on_delete=models.CASCADE)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=True, verbose_name='Percentual')

    class Meta:
        verbose_name_plural = 'Impostos Produtos NCM'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'fk_taxes',
                    'fk_ncmcodes'
                ],
                name='pk_ncmtaxes'
            )
        ]

    def __str__(self):
        return self.fk_taxes.fk_type_taxes.name_tax + ' - ' + self.fk_ncmcodes.name_ncm
