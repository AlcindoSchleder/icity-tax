from django.db import models


class UsersTests(models.Model):
    pk_users_tests = models.CharField(max_length=255, primary_key=True, verbose_name='e-Mail')
    user_name = models.CharField(max_length=150, verbose_name='Nome')
    qtd_tests = models.IntegerField(verbose_name='Quant.')

    class Meta:
        db_table = 'home_users_tests'
        verbose_name_plural = 'Testes da API'

    def __str__(self):
        return self.pk_users_tests + ' tests: {:d}'.format(self.qtd_tests)


class UsersContacts(models.Model):
    pk_users_contacts = models.AutoField(primary_key=True, verbose_name='Código')
    user_email = models.CharField(max_length=255, verbose_name='e-Mail')
    user_name = models.CharField(max_length=150, verbose_name='Nome')
    subject = models.CharField(max_length=200, verbose_name='Assunto')
    message = models.TextField(verbose_name='Mensagem')

    class Meta:
        db_table = 'home_users_contacts'
        verbose_name_plural = 'Contatos'

    def __str__(self):
        return self.user_email + ' - ' + self.subject
