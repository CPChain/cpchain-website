# Generated by Django 2.2.2 on 2020-07-14 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_ip', '0003_auto_20200714_0547'),
    ]

    operations = [
        migrations.AddField(
            model_name='ip',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ip',
            name='country',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ip',
            name='countryCode',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='ip',
            name='isp',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ip',
            name='region',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='ip',
            name='regionName',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ip',
            name='timezone',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
