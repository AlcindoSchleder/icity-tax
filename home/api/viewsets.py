import json
import jwt

from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UsersTestsSerializer, UsersTestsSerializer
from home.models import UsersTests, UsersContacts

from icity_tax.settings import SECRET_KEY, MAX_USER_TESTS
from icity_tax.utils import check_captcha


class UsersTestsTokensViewSet(viewsets.ViewSet):

    @authentication_classes([])
    @permission_classes([])
    def check_permissions(self, request):
        super(UsersTestsTokensViewSet, self).check_permissions(request)

    def perform_authentication(self, request):
        newUser = authenticate(username='test_demo', password=SECRET_KEY)
        if not newUser:
            return Response({'message': 'Forbidden! system user not found!'}, 403)
        if not newUser.is_active:
            return Response({'message': 'Forbidden! system user not active!'}, 403)
        login(request, newUser)
        super(UsersTestsTokensViewSet, self).perform_authentication(request)

    # @action(methods=['POST', 'GET'], detail=False)
    @action(methods=['POST'], detail=False)
    def gen_test_token(self, request):
        """
        Return a token by data sended into payload
        """
        # captcha_result = check_captcha(request)
        # if captcha_result['status'] != 200:
        #     return Response(captcha_result, captcha_result['status'])

        user_name = request.data['username']
        user_mail = request.data['usermail']
        qsTests = UsersTests.objects.filter(pk_users_tests=user_mail)
        if qsTests:
            if len(qsTests) > 0:
                qsTests = qsTests[0]
            qtd_tests = qsTests.qtd_tests
            if qtd_tests > MAX_USER_TESTS:
                return Response({'message': 'Forbidden! Number of tests exceeded for this email!'}, 403)
            qsTests.qtd_tests = qtd_tests + 1
            qsTests.save()
        else:
            UsersTests.objects.create(
                pk_users_tests=user_mail,
                user_name=user_name,
                qtd_tests=1
            )
        logout(request)

        payload = {
            'iss': 'https://tax.icity.net.br/',
            'sub': 0,
            'iat': datetime.now(),
            'exp': datetime.now() + timedelta(seconds=300),
            'aud': 'i-city Tax',
            'user_name': request.data['username'],
            'user_mail': request.data['usermail'],
        }

        token = jwt.api_jwt.encode(payload, SECRET_KEY, 'HS256')
        data = {
            'token': token.decode("utf-8")
        }
        return Response(json.dumps(data), content_type="application/json")

    @action(methods=['GET'], detail=False)
    def query_test_tax(self, request):
        auth = request.headers['authorization'].split(' ')
        data = request.query_params
        try:
            if auth[0] != data['token-access']:
                return Response({'message': 'Erro critico!! O token do header não correspende a um token jwt: ' + auth[1]}, 403)
            result = {}
            if auth[0] == 'token':
               result = jwt.api_jwt.decode(auth[1], SECRET_KEY, algorithms='HS256')
        except Exception as e:
            return Response({'message': 'Erro ao confirmar o token: ' + auth[1] + ' erro: ' + e}, 403)
        if not result:
            return Response({'message': 'API não autorizada (token)!'}, 401)
        return Response({'message': 'Forbidden!', 'getData': data}, 403)


class UsersTestsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that generate a temporary jwt token for tests.
    """
    serializer_class = UsersTestsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def list(self, request, *args, **kwargs):
        """
        Returns a list of registers for the queryset
        """
        if not request.auth:
            return Response({'message': 'Invalid credentials (login)!'}, 401)
        if not request.auth.user.is_superuser:
            return Response({'message': 'Restriced Action!'}, 401)
        return super(UsersTestsViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Returns a record with filtered by email
        """
        if not request.auth and not request.auth.user.is_superuser:
            return Response({'message': 'Restriced Action!'}, 401)
        return super(UsersTestsViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Insert a register
        """
        if not request.auth and not request.auth.user.is_superuser:
            return Response({'message': 'Restriced Action!'}, 401)
        return super(UsersTestsViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a register
        """
        if not request.auth and not request.auth.user.is_superuser:
            return Response({'message': 'Restriced Action!'}, 401)
        return super(UsersTestsViewSet, self).destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update a register
        """
        if not request.auth and request.auth.user.is_superuser:
            return Response({'message': 'Restriced Action!'}, 401)
        return super(UsersTestsViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Update a register partialy
        """
        if not request.auth and request.auth.user.is_superuser:
            return Response({'message': 'Restriced Action!'}, 401)
        return super(UsersTestsViewSet, self).partial_update(request, *args, **kwargs)

