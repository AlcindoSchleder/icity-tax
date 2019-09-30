# Generated by Django 2.2.5 on 2019-09-29 05:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('pk_countries', models.SmallIntegerField(primary_key=True, serialize=False, verbose_name='Código DDI: ')),
                ('name_country', models.CharField(max_length=100, verbose_name='Nome: ')),
                ('country_symbol', models.CharField(default='', max_length=5, verbose_name='Símbolo do País: ')),
            ],
            options={
                'verbose_name_plural': 'Países',
            },
        ),
        migrations.CreateModel(
            name='Languages',
            fields=[
                ('pk_language', models.CharField(max_length=5, primary_key=True, serialize=False, verbose_name='Símbolo: ')),
                ('name_laguage', models.CharField(max_length=50, verbose_name='Descrição: ')),
            ],
            options={
                'verbose_name_plural': 'Linguagens',
            },
        ),
        migrations.CreateModel(
            name='States',
            fields=[
                ('pk_states', models.CharField(max_length=5, primary_key=True, serialize=False, verbose_name='Código do País/UF: ')),
                ('state_symbol', models.CharField(max_length=2, verbose_name='UF: ')),
                ('name_state', models.CharField(max_length=100, verbose_name='Nome: ')),
                ('time_zone', models.CharField(default='America/Sao_Paulo', max_length=50, verbose_name='Fuso Horário: ')),
                ('kc_cities', models.IntegerField(default=0, verbose_name='Cities KeyControl')),
                ('fk_countries', models.ForeignKey(default=55, on_delete=django.db.models.deletion.CASCADE, to='localization.Countries', verbose_name='País: ')),
            ],
            options={
                'verbose_name_plural': 'Estados',
            },
        ),
        migrations.AddField(
            model_name='countries',
            name='fk_languages',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='localization.Languages', verbose_name='Língua Oficial: '),
        ),
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('pk_cities', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='Código: ')),
                ('name_city', models.CharField(max_length=150, verbose_name='Nome: ')),
                ('zip_code', models.CharField(max_length=15, verbose_name='C.E.P.: ')),
                ('fk_countries', models.ForeignKey(default=55, on_delete=django.db.models.deletion.CASCADE, to='localization.Countries', verbose_name='País: ')),
                ('fk_states', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='localization.States', verbose_name='Estado: ')),
            ],
            options={
                'verbose_name_plural': 'Cidades',
            },
        ),
    ]
