"""

chain models

"""

from django.db import models


# class AddressMarkType(models.Model):
#     """ 地址标记类型
#     """
#     name = models.CharField(max_length=30, help_text='类型名称', unique=True)
#     description = models.CharField(max_length=500)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class AddressMark(models.Model):
#     """ 地址标记
#     """
#     name = models.CharField(max_length=30, help_text='标记名称')
#     logo = models.ImageField(upload_to='img/addresses', null=True, blank=True)
#     type_id = models.IntegerField(help_text='标记类型 ID')
#     url = models.URLField(null=True, help_text='跳转地址')
#     description = models.CharField(max_length=500)
#     is_public = models.BooleanField(help_text='是否公开')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
