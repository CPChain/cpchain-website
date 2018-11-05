from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

PARTNERS = (('Partners', 'Partners'), ('Investors', 'Investors'), ('Exchanges', 'Exchanges'))
NEWS_CATEGORY = (
    ('Community Updates', 'Community Updates'), ('AMA Sessions', 'AMA Sessions'), ('Media Reports', 'Media Reports'))


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

    def __str__(self):
        return self.name


class Partner(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='img/Partners')
    link = models.CharField(max_length=100)
    type = models.CharField(choices=PARTNERS, max_length=20)

    def __str__(self):
        return self.name


class New(models.Model):
    category = models.CharField(choices=NEWS_CATEGORY, max_length=50)
    title = models.CharField(max_length=50)
    banner = models.ImageField(upload_to='img/News',null=True)
    update_time = models.DateField()
    content = RichTextUploadingField(default='')

    def __str__(self):
        return self.title
