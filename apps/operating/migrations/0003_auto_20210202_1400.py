# Generated by Django 2.2.2 on 2021-02-02 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operating', '0002_auto_20201228_1809'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='templates',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='templates',
            name='deleted',
            field=models.BooleanField(default=False, help_text='删除标志'),
        ),
    ]