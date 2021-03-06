from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

NEWS_CATEGORY = (
    ('News_en', 'News_en'),
    ('News_cn', 'News_cn'),
    ('Event_en', 'Event_en'),
    ('Event_cn', 'Event_cn'),
    ('draft', 'draft'))


# Create your models here.
class WalletNew(models.Model):
    category = models.CharField(choices=NEWS_CATEGORY, max_length=50)
    title = models.CharField(max_length=200)
    banner = models.ImageField(upload_to='img/Wallet', null=True, blank=True)
    update_time = models.DateField()
    content = RichTextUploadingField(blank=True, null=True, default='', external_plugin_resources=[('youtube',
                                                                                                    '/static/youtube/',
                                                                                                    'plugin.js'), (
                                                                                                       'imageresize',
                                                                                                       '/static/imageresize/',
                                                                                                       'plugin.js')])

    def __str__(self):
        return self.title


#
class SwipeBanner(models.Model):
    news = models.ForeignKey(WalletNew, on_delete=models.CASCADE)
    lang = models.CharField(choices=(('en', 'en'), ('cn', 'cn')), default='en', max_length=50)
    index_banner = models.ImageField(upload_to='img/Wallet', null=False, blank=False)
    banner_time = models.DateField()
    is_active = models.BooleanField('Active', default=True)

    def __str__(self):
        return self.news.title


class FAQ(models.Model):
    title = models.CharField(max_length=200)
    lang = models.CharField(choices=(('en', 'en'), ('zh', 'zh')), default='en', max_length=50)
    weight = models.IntegerField(default=0)
    content = RichTextUploadingField(blank=True, null=True, default='', external_plugin_resources=[('youtube',
                                                                                                    '/static/youtube/',
                                                                                                    'plugin.js'), ])
    isActive = models.BooleanField('Active', default=True)

    def __str__(self):
        return self.title


class Term(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextUploadingField(blank=True, null=True, default='', external_plugin_resources=[('youtube',
                                                                                                    '/static/youtube/',
                                                                                                    'plugin.js')])

    def __str__(self):
        return self.title
