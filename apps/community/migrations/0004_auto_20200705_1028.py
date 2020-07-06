# Generated by Django 2.2.2 on 2020-07-05 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0003_auto_20200705_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='client_id',
            field=models.CharField(blank=True, help_text='客户端 ID', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='period',
            field=models.IntegerField(editable=False, help_text='等待时间，单位为秒', null=True),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='proposer_addr',
            field=models.CharField(default='', editable=False, help_text='发起人地址', max_length=100),
        ),
    ]