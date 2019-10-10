from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

PARTNERS = (('Partners', 'Partners'), ('Investors', 'Investors'), ('Exchanges', 'Exchanges'), ('Industry', 'Industry'),
            ('Project', 'Project'), ('Academia', 'Academia'), ('Capital', 'Capital'), ('Association', 'Association'),
            ('IndustryNode', 'IndustryNode'))

Media_CATEGORY = (('Media Reports', 'Media Reports'),
                  ('媒体报道', '媒体报道'))
NEWS_CATEGORY = (
    ('Community Updates', 'Community Updates'), ('Community Events', 'Community Events'),
    ('Official Announcement', 'Official Announcement'),
    ('项目进展', '项目进展'), ('重大发布', '重大发布'), ('draft', 'draft'))


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
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class New(models.Model):
    category = models.CharField(choices=NEWS_CATEGORY, max_length=50)
    title = models.CharField(max_length=200)
    banner = models.ImageField(upload_to='img/News', null=True, blank=True)
    update_time = models.DateField()
    summary = models.CharField(max_length=500, blank=True, null=True, default='')
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
    link = models.CharField(max_length=500, default='http://')
    media_logo = models.ImageField(upload_to='img/MediaLogo', null=True, blank=True)
    media_name = models.CharField(max_length=200, default='')
    summary = models.CharField(max_length=500, blank=True, null=True, default='')


class Notification(models.Model):
    content = models.CharField(max_length=400)
    content_en = models.CharField(max_length=400)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    url = models.CharField(max_length=500, default='http://', null=True, blank=True)


class IndexVideo(models.Model):
    url = models.CharField(max_length=400, default='https://')
    url_en = models.CharField(max_length=400, default='https://')
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    time = models.DateTimeField()
    ispublish = models.BooleanField(default=True)
    weight = models.IntegerField(default=0)
    time = models.DateTimeField()
    placeHolderTime = models.FloatField()
