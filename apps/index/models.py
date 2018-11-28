from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

PARTNERS = (('Partners', 'Partners'), ('Investors', 'Investors'), ('Exchanges', 'Exchanges'))
NEWS_CATEGORY = (
    ('Community Updates', 'Community Updates'), ('AMA Sessions', 'AMA Sessions'),
    ('项目进展', '项目进展'), ('重大发布', '重大发布'),)
Media_CATEGORY = (('Media Reports', 'Media Reports'),
                  ('媒体报道', '媒体报道'))


class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class TeamMate(models.Model):
    name = models.CharField(max_length=50)
    name_zh = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=50)
    title_zh = models.CharField(max_length=50)
    image = models.ImageField(upload_to='img/Team', max_length=100, null=True, blank=True)
    desc = models.CharField(max_length=500, null=True, blank=True)
    desc_zh = models.CharField(max_length=500, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Partner(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='img/Partners')
    link = models.CharField(max_length=200)
    type = models.CharField(choices=PARTNERS, max_length=20)

    def __str__(self):
        return self.name


class New(models.Model):
    category = models.CharField(choices=NEWS_CATEGORY, max_length=50)
    title = models.CharField(max_length=200)
    banner = models.ImageField(upload_to='img/News', null=True, blank=True)
    update_time = models.DateField()
    content = RichTextUploadingField(blank=True, null=True, default='', external_plugin_resources=[('youtube',
                                                                                                    '/static/youtube/',
                                                                                                    'plugin.js')])

    def __str__(self):
        return self.title


class Media(models.Model):
    category = models.CharField(choices=Media_CATEGORY, max_length=50)
    title = models.CharField(max_length=200)
    banner = models.ImageField(upload_to='img/News', null=True, blank=True)
    update_time = models.DateField()
    link = models.CharField(max_length=500)
    media_logo = models.ImageField(upload_to='img/MediaLogo', null=True, blank=True)
    media_name = models.CharField(max_length=200)
    summary = models.CharField(max_length=500)
