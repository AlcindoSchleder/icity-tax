from django.db import models

# Create your models here.


class Languages(models.Model):
    pk_language = models.CharField(max_length=5, primary_key=True, verbose_name='Símbolo: ')
    name_laguage = models.CharField(max_length=50, verbose_name='Descrição: ')

    class Meta:
        verbose_name_plural = "Linguagens"

    def __str__(self):
        return self.name_laguage


class Countries(models.Model):
    pk_countries = models.SmallIntegerField(primary_key=True, verbose_name='Código DDI: ')
    fk_languages = models.ForeignKey(Languages, on_delete=models.PROTECT, verbose_name='Língua Oficial: ')
    name_country = models.CharField(max_length=100, verbose_name='Nome: ')
    country_symbol = models.CharField(max_length=5, default='', verbose_name='Símbolo do País: ')

    class Meta:
        verbose_name_plural = "Países"

    def __str__(self):
        return self.name_country


class States(models.Model):
    pk_states = models.CharField(max_length=5, primary_key=True, verbose_name='Código do País/UF: ')
    fk_countries = models.ForeignKey(Countries, default=55, on_delete=models.CASCADE, verbose_name='País: ')
    state_symbol = models.CharField(max_length=2, verbose_name='UF: ')
    name_state = models.CharField(max_length=100, verbose_name='Nome: ')
    time_zone = models.CharField(max_length=50, verbose_name='Fuso Horário: ', default='America/Sao_Paulo')
    kc_cities = models.IntegerField(default=0, verbose_name='Cities KeyControl')

    class Meta:
        verbose_name_plural = "Estados"

    @property
    def country(self):
        return self.fk_countries.name_country

    def __str__(self):
        return self.fk_countries.name_country + ' / ' + self.state_symbol


def before_save_state(instance, created=False, **kwargs):
    if created:
        instance.kc_cities = 0
    pk = str(instance.fk_countries_id) + '.' + instance.state_symbol
    if instance.pk_states != pk:
        instance.pk_states = pk


models.signals.pre_save.connect(before_save_state, sender=States, dispatch_uid='before_save_state')


class Cities(models.Model):
    pk_cities = models.CharField(max_length=15, primary_key=True, verbose_name='Código: ')
    fk_states = models.ForeignKey(
        States,
        default='',
        on_delete=models.CASCADE,
        verbose_name='Estado: '
    )
    name_city = models.CharField(max_length=150, verbose_name='Nome: ')
    zip_code = models.CharField(max_length=15, verbose_name='C.E.P.: ')

    class Meta:
        verbose_name_plural = "Cidades"

    @property
    def country(self):
        return self.fk_states.country

    @property
    def state(self):
        return self.fk_states.state_symbol

    @property
    def flag_add(self):
        return self.objects._state.adding

    def __str__(self):
        return self.name_city + ' - ' + self.country + ' / ' + self.state


def before_save_city(instance, **kwargs):
    created = instance._state.adding
    if not created:
        return
    try:
        qsStates = States.objects.get(pk_states=instance.fk_states_id);
        if qsStates:
            kc = qsStates.kc_cities
            kc += 1
            qsStates.kc_cities = kc
            qsStates.save()
            pk = instance.fk_states_id + '.' + str(kc)
            if instance.pk_cities != pk:
                instance.pk_cities = pk
    except Exception as e:
        kc = 0


models.signals.pre_save.connect(before_save_city, sender=Cities, dispatch_uid='before_save_city')
