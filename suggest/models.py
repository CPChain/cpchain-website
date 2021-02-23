from django.db import models

class Suggest(models.Model):
    description = models.CharField(help_text="建议内容", blank=False, max_length=500)
    email = models.EmailField(help_text='用户 email')
    platform = models.CharField(help_text='提交平台：android/ios/browser 等', max_length=20)
    handled = models.BooleanField(help_text='是否已处理', null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
