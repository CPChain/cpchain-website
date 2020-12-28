"""

operating models

"""

from django.db import models

class TemplateType(models.Model):
    """ 模板类型
    """
    name = models.CharField(max_length=30, help_text='类型名称', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Templates(models.Model):
    """ 运营模板
    """
    name = models.CharField(max_length=30, help_text='模板名称', null=False, unique=True)
    type_id = models.IntegerField(help_text='模板类型 ID', null=True)
    template = models.TextField(help_text='模板内容', blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
