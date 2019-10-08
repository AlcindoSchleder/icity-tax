from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from localization.models import States
from taxes.models import Taxes, NcmTaxes
from customers.models import Customers
from .serializers import TaxesSerializer


class TaxesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    serializer_class = TaxesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        typeTax = self.request.query_params.get('type_tax')
        getOrigin = self.request.query_params.get('get_origin')
        country = self.request.query_params.get('country')
        state = country + '.' + self.request.query_params.get('state')
        product_ncm = self.request.query_params.get('product_ncm')
        fromUser = None
        if getOrigin:
            pkUser = self.request.auth.user.id
            fromUser = Customers.get_orgin_data(pkUser)
        qsTaxes = Taxes.objects.all()
        if typeTax:
            qsTaxes = qsTaxes.filter(fk_type_taxes_id=typeTax)
        if fromUser:
            qsTaxes = qsTaxes.filter(
                fk_countries_origin_id=fromUser['country'],
                fk_states_origin_id=fromUser['state']
            )
        if country and state:
            qsTaxes = qsTaxes.filter(
                fk_countries_destiny_id=fromUser['country'],
                fk_states_destiny_id=fromUser['state']
            )
        qsNcmTaxes = NcmTaxes.objects.filter(pk_ncmtaxes_id__in=qsTaxes)
        if product_ncm:
            qsNcmTaxes = qsNcmTaxes.filter(fk_ncmcodes=product_ncm)
        return qsNcmTaxes

    def list(self, request, *args, **kwargs):
        """
        Returns a list of registers for the queryset
        """
        if not request.auth and not request.auth.user.is_superuser:
            return Response({'message': 'Restriced Action!'}, 401)
        return super(TaxesViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Returns a record with filtered by pk_toursspots
        """
        if not request.auth and not request.auth.user.is_superuser:
            return Response({'message': 'Restriced Action!'}, 401)
        return super(TaxesViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Insert a register
        """
        if not request.auth and not request.auth.user.is_superuser:
            return Response({'message': 'Restriced Action!'}, 401)
        return super(TaxesViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a register
        """
        if not request.auth and not request.auth.user.is_superuser:
            return Response({'message': 'Restriced Action!'}, 401)
        return super(TaxesViewSet, self).destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update a register
        """
        if not request.auth and request.auth.user.is_superuser:
            return Response({'message': 'Restriced Action!'}, 401)
        return super(TaxesViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Update a register partialy
        """
        if not request.auth and request.auth.user.is_superuser:
            return Response({'message': 'Restriced Action!'}, 401)
        return super(TaxesViewSet, self).partial_update(request, *args, **kwargs)

    @action(methods=['POST'], detail=False)
    def product_tax(self, request):
        """
        Update a register partialy
        """
        if not request.auth:
            return Response({'message': 'Invalid credentials (login)!'}, 401)
        user_pk = request.auth.user.id

        from_user = Customers.get_orgin_data(user_pk)
        if 'message' in from_user.keys():
            return Response(from_user, from_user['status'])

        country = request.data['country']
        state = request.data['state']
        product_ncm = request.data['product_ncm']

        qsState = States.objects.filter(pk_states=str(country) + '.' + state)
        if not qsState:
            return Response({'message': 'Invalid Destination!'}, 401)

        return Response(NcmTaxes.set_result_to_response(
            qsState,
            from_user['country_origin'],
            from_user['state_origin'],
            from_user['from_user'],
            country,
            state,
            product_ncm
        ))
