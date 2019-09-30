# Generated by Django 2.2.5 on 2019-09-30 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('localization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('pk_categories', models.AutoField(primary_key=True, serialize=False, verbose_name='Código')),
                ('name_cat', models.CharField(max_length=50, verbose_name='Descrição')),
                ('flag_tcat', models.SmallIntegerField(choices=[(1, 'Administrador'), (2, 'Cliente'), (3, 'Consumidor'), (4, 'Fornecedor'), (5, 'Funcionário')], default=2, verbose_name='Tipo de Categoria')),
                ('flag_repr', models.BooleanField(default=False, verbose_name='Representante')),
            ],
            options={
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.CreateModel(
            name='Registers',
            fields=[
                ('pk_registers', models.AutoField(primary_key=True, serialize=False, verbose_name='Código')),
                ('flag_treg', models.SmallIntegerField(choices=[(1, 'Pessoa Física'), (2, 'Pessoa Jurídica')], verbose_name='Tipo')),
                ('main_doc', models.CharField(max_length=20, unique=True, verbose_name='Documento de Identificação')),
                ('secondary_doc', models.CharField(max_length=30, verbose_name='Outro Documento')),
                ('first_name', models.CharField(max_length=50, verbose_name='Primeiro Nome')),
                ('last_name', models.CharField(max_length=50, verbose_name='Sobrenome')),
                ('alias_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nome Fantasia')),
                ('enterprise_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nome da Empresa')),
                ('insert_date', models.DateTimeField(auto_now_add=True, verbose_name='Data do Cadastro')),
                ('kc_registers_address', models.SmallIntegerField(default=0, verbose_name='KeyControl RegistersAddresses')),
            ],
            options={
                'verbose_name_plural': 'Usuários',
            },
        ),
        migrations.CreateModel(
            name='RegistersCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flag_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('insert_date', models.DateTimeField(auto_now_add=True, verbose_name='Data de inclusão')),
                ('fk_categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registers.Categories', verbose_name='Categoria')),
                ('fk_registers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registers.Registers', verbose_name='Pessoa/Empresa')),
            ],
            options={
                'verbose_name_plural': 'Categorias do Usuário',
            },
        ),
        migrations.CreateModel(
            name='RegistersAddress',
            fields=[
                ('pk_registers_address', models.IntegerField(primary_key=True, serialize=False, verbose_name='Código')),
                ('flag_taddr', models.SmallIntegerField(choices=[(1, 'Endereço Residencial'), (2, 'Endereço Comercial'), (3, 'Endereço de Cobrança'), (4, 'Endereço de Entrega')], default=1, verbose_name='Typo')),
                ('flag_default', models.BooleanField(default=False, verbose_name='Default')),
                ('address', models.CharField(max_length=100, verbose_name='Endereço')),
                ('number', models.IntegerField(verbose_name='Número')),
                ('complement', models.CharField(blank=True, max_length=100, null=True, verbose_name='Complemento')),
                ('quarter', models.CharField(max_length=50, verbose_name='Bairro')),
                ('zip_code', models.CharField(max_length=15, verbose_name='C.E.P.')),
                ('fk_cities', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='localization.Cities', verbose_name='Cidade')),
                ('fk_registers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registers.Registers', verbose_name='Usuário')),
            ],
            options={
                'verbose_name_plural': 'Endereços',
            },
        ),
        migrations.AddField(
            model_name='registers',
            name='fk_categories',
            field=models.ManyToManyField(help_text='Selecione as categorias a qual este usuário pertence. Elas são criadas sempre como ativas, posteriormente pode-se alterar o campo "ativo" no menu "Categorias do Usuário".', related_name='categories', through='registers.RegistersCategories', to='registers.Categories', verbose_name='Categorias'),
        ),
        migrations.AddField(
            model_name='registers',
            name='fk_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Login do Usuário'),
        ),
        migrations.AddIndex(
            model_name='registersaddress',
            index=models.Index(fields=['fk_cities', 'zip_code'], name='localization_idx'),
        ),
    ]
