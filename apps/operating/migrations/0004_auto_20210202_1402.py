# Generated by Django 2.2.2 on 2021-02-02 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operating', '0003_auto_20210202_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templates',
            name='deleted',
            field=models.BooleanField(default=False, help_text='删除标志', null=True),
        ),
    ]