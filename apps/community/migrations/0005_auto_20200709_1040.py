# Generated by Django 2.2.2 on 2020-07-09 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0004_auto_20200705_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='proposer_addr',
            field=models.CharField(default='', help_text='发起人地址', max_length=100),
        ),
    ]
