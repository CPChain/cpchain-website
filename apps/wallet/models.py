from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

NEWS_CATEGORY = (
    ('News_en', 'News_en'),
    ('News_cn', 'News_cn'),
    ('draft', 'draft'))


# Create your models here.
class WalletNews(models.Model):
    category = models.CharField(choices=NEWS_CATEGORY, max_length=50)
    title = models.CharField(max_length=200)
    banner = models.ImageField(upload_to='img/Wallet', null=True, blank=True)
    update_time = models.DateField()
    content = RichTextUploadingField(blank=True, null=True, default='', external_plugin_resources=[('youtube',
                                                                                                    '/static/youtube/',
                                                                                                    'plugin.js')])

    def __str__(self):
        return self.title
