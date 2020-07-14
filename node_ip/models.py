"""

models.py

"""

from django.db import models

class IP(models.Model):
    ip = models.GenericIPAddressField(max_length=100, help_text='ip', unique=True)
    latitude = models.FloatField(help_text='latitude/纬度', null=True)
    longitude = models.FloatField(help_text='longitude/经度', null=True)
    handled = models.BooleanField(default=False, help_text='是否已处理，即获取到经纬度')
    deleted = models.BooleanField(default=False, help_text='是否已删除')
    country = models.CharField(max_length=100, null=True)
    countryCode = models.CharField(max_length=20, null=True)
    region = models.CharField(max_length=20, null=True)
    regionName = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    isp = models.CharField(max_length=100, null=True)
    timezone = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
