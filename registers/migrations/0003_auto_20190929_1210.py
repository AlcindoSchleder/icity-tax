# Generated by Django 2.2.5 on 2019-09-29 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registers', '0002_auto_20190929_0424'),
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
            name='RegistersCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flag_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('insert_date', models.DateTimeField(auto_now_add=True, verbose_name='Data de inclusão')),
                ('fk_categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registers.Categories', verbose_name='Categoria')),
                ('fk_registers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registers.Registers', verbose_name='Pessoa/Empresa')),
            ],
            options={
                'verbose_name_plural': 'Vinclulo das Categorias',
            },
        ),
        migrations.AddField(
            model_name='registers',
            name='fk_categories',
            field=models.ManyToManyField(through='registers.RegistersCategories', to='registers.Categories', verbose_name='Categorias'),
        ),
    ]