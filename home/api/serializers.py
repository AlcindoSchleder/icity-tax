from rest_framework import serializers
from home.models import UsersContacts, UsersTests


class UsersTestsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UsersTests
        fields = ['pk_users_tests', 'user_mail', 'qtd_tests']


class UsersContactsSerializer(serializers.HyperlinkedIdentityField):
    class Meta:
        model = UsersContacts
        fields = ['user_email', 'user_name', 'subject', 'messages']
