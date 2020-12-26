"""

serializers

"""

from django.db.models import fields
from rest_framework import serializers

from .models import TemplateType, Templates

class TemplateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateType
        fields = '__all__'

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Templates
        fields = '__all__'
