# Generated by Django 2.2.5 on 2019-09-30 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='ncmtaxes',
            name='pk_taxes',
        ),
        migrations.AddConstraint(
            model_name='ncmtaxes',
            constraint=models.UniqueConstraint(fields=('fk_taxes', 'fk_ncmcodes'), name='pk_ncmtaxes'),
        ),
    ]
