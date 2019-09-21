from django.db import models

# Create your models here.


class Languages(models.Model):
    pk_language = models.CharField(max_length=5, primary_key=True, verbose_name='Símbolo: ')
    name_laguage = models.CharField(max_length=50, verbose_name='Descrição: ')

    class Meta:
        verbose_name_plural = "Languages"

    def __str__(self):
        return self.name_laguage


class Countries(models.Model):
    pk_countries = models.SmallIntegerField(primary_key=True, verbose_name='Código DDI: ')
    fk_languages = models.ForeignKey(Languages, on_delete=models.PROTECT, verbose_name='Língua Oficial: ')
    name_country = models.CharField(max_length=100, verbose_name='Nome: ')

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name_country


class Provinces(models.Model):
    pk_provinces = models.CharField(max_length=5, verbose_name='Símbolo da UF: ')
    fk_countries = models.ForeignKey(Countries, on_delete=models.CASCADE, verbose_name='País: ')
    name_province = models.CharField(max_length=100, verbose_name='Nome: ')
    country_symbol = models.CharField(max_length=5, verbose_name='Símbolo do País: ')
    time_zone = models.CharField(max_length=50, verbose_name='Fuso Horário: ', default='America/Sao_Paulo')

    class Meta:
        verbose_name_plural = "Provinces"
        unique_together = ('pk_provinces', 'fk_countries')

    @property
    def country(self):
        return self.fk_countries.country_symbol

    def __str__(self):
        return self.fk_countries.name_coutry + ' - ' + self.pk_provinces


class Cities(models.Model):
    pk_cities = models.AutoField(primary_key=True, verbose_name='Código: ')
    fk_provinces = models.ForeignKey(Provinces, on_delete=models.CASCADE, verbose_name='Estado')
    name_city = models.CharField(max_length=150, verbose_name='Nome: ')
    zip_code = models.CharField(max_length=15, verbose_name='C.E.P.: ')

    class Meta:
        verbose_name_plural = "Cities"
        unique_together = ('fk_provinces', 'pk_cities')

    @property
    def country(self):
        return self.fk_provinces.country

    def state(self):
        return self.fk_provinces.pk_provinces

    def __str__(self):
        return self.name_city + ' - ' + self.country + ' / ' + self.state
