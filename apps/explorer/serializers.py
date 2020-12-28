"""

chain serializers

"""

from django.db.models import fields
from rest_framework import serializers

from .models import AddressMark, AddressMarkType


class AddressMarkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressMarkType
        fields = '__all__'


class AddressMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressMark
        fields = '__all__'
