"""

serializers

"""

from rest_framework import serializers

from .models import TemplateType, Templates

class TemplateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateType
        fields = '__all__'

def tmpl_name_validator(name):
    if len(name) < 3:
        raise Exception('模板名称不能少于 3 个字')
    return name

class TemplateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30, validators=[tmpl_name_validator,])
    class Meta:
        model = Templates
        fields = '__all__'
