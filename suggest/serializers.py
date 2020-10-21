
from rest_framework import serializers

from .models import Suggest

class SuggestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggest
        fields = '__all__'
