from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from localization.models import States
from taxes.models import Taxes, NcmTaxes
from registers.models import Registers, RegistersAddress
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
        country = self.request.query_params.get('country')
        state = country + '.' + self.request.query_params.get('state')
        product_ncm = self.request.query_params.get('product_ncm')

        return self.load_data_from_db(country, state, product_ncm)

    def list(self, request, *args, **kwargs):
        """
        Returns a list of registers for the queryset
        """
        if not request.auth:
            return Response({'message': 'Invalid credentials (login)!'}, 401)
        if not request.auth.user.is_superuser:
            return Response({'message': 'Restriced Action!'}, 401)
        user_pk = request.auth.user.id
        register = Registers.objects.get(fk_user_id=user_pk)
        if not register:
            return Response({'message': 'Invalid credentials (registers)!'}, 401)
        customer = Customers.objects.get(fk_registers_id=register.pk_registers)
        if not customer:
            return Response({'message': 'Invalid credentials (customers)!'}, 401)
        if customer.flag_block:
            return Response({'message': 'User blocked!'}, 401)
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

    def get_address_from_pk(self, pk):
        list_codes = pk.split('.')
        return list_codes[0], list_codes[1]

    def get_orgin_data(self, user_pk):
        register = Registers.objects.filter(fk_user_id=user_pk)
        if not register:
            return Response({'message': 'Invalid credentials (registers)!'}, 401)
        if len(register) > 0:
            register = register[0]
        address = RegistersAddress.objects.filter(fk_registers_id=register.pk_registers)
        address_default = address.filter(flag_default=True)
        if address_default:
            if len(address_default) > 0:
                address = address_default[0]
            country_origin, state_origin = self.get_address_from_pk(address_default.fk_cities_id)
            address = address_default
        elif address:
            if len(address) > 0:
                address = address[0]
            country_origin, state_origin = self.get_address_from_pk(address.fk_cities_id)
        else:
            return Response({'message': 'Invalid credentials (Origin)!'}, 401)
        customer = Customers.objects.filter(fk_registers_id=register.pk_registers)
        if not customer:
            return Response({'message': 'Invalid credentials (customers)!'}, 401)
        if len(customer) > 0:
            customer = customer[0]
        if customer.flag_block:
            return Response({'message': 'User blocked!'}, 401)
        return {
            'country_origin': country_origin,
            'state_origin': state_origin,
            'from_user': register.name_register + ' - ' + address.country + '/' + address.state
        }

    def set_result_to_response(
        self,
        qs,
        country_origin,
        state_origin,
        from_user,
        country,
        state,
        product_ncm
    ):
        if len(qs) > 0:
            qsState = qs[0]

        to_client = str(qsState)
        return {
            'message': 'Product not found!.',
            'from': from_user,
            'to': to_client,
            'product_ncm': product_ncm,
            'taxes': self.load_data_from_db(
                country_origin,
                state_origin,
                country,
                state,
                product_ncm
            )
        }

    def load_data_from_db(
        self,
        country_origin,
        state_origin,
        country,
        state,
        product
    ):
        qsTaxes = Taxes.objects.filter(
            fk_countries_origin=country_origin,
            fk_states_origin=str(country_origin) + '.' + state_origin,
            fk_countries_destiny=country,
            fk_states_destiny=str(country) + '.' + state,
        )
        taxes_list = []
        for tax in qsTaxes:
            qsTax = NcmTaxes.objects.filter(
                fk_taxes=tax,
                fk_ncmcodes=product
            )
            tax = {
                'type_tax': str(tax.fk_type_taxes),
                'tax': tax.taxdef
            }
            if qsTax:
                tax['atx'] = qsTax.tax
            taxes_list.append(tax)
        return taxes_list

    @action(methods=['POST'], detail=False)
    def product_tax(self, request):
        """
        Update a register partialy
        """
        if not request.auth:
            return Response({'message': 'Invalid credentials (login)!'}, 401)
        user_pk = request.auth.user.id

        from_user = self.get_orgin_data(user_pk)
        if 'message' in from_user.keys():
            return from_user

        country = request.data['country']
        state = request.data['state']
        product_ncm = request.data['product_ncm']

        qsState = States.objects.filter(pk_states=str(country) + '.' + state)
        if not qsState:
            return Response({'message': 'Invalid Destination!'}, 401)

        return Response(self.set_result_to_response(
            qsState,
            from_user['country_origin'],
            from_user['state_origin'],
            from_user['from_user'],
            country,
            state,
            product_ncm
        ))
