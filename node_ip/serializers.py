"""

serializers.py

"""

from rest_framework import serializers

from .models import IP

class IPSerializer(serializers.ModelSerializer):

    class Meta:
        model = IP
        fields = ['ip', 'latitude', 'longitude']
        extra_kwargs = {
            'latitude': {'read_only': True},
            'longitude': {'read_only': True},
        }
