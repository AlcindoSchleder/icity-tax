from rest_framework import serializers
from taxes.models import Taxes


class TaxesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Taxes
        fields = ['country', 'province', 'tax']
