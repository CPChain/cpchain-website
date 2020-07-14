"""

models.py

"""

from django.db import models

class IP(models.Model):
    ip = models.CharField(max_length=100, help_text='ip')
    latitude = models.FloatField(help_text='latitude/纬度')
    longitude = models.FloatField(help_text='longitude/经度')
    handled = models.BooleanField(default=False, help_text='是否已处理，即获取到经纬度')
    deleted = models.BooleanField(default=False, help_text='是否已删除')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
