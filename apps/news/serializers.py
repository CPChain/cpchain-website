"""

News serializers

"""

from rest_framework import serializers
from apps.index.models import New

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = New
        fields = '__all__'

class NewsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = New
        exclude = ['content']
