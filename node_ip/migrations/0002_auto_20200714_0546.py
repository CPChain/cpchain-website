# Generated by Django 2.2.2 on 2020-07-14 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_ip', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ip',
            name='ip',
            field=models.GenericIPAddressField(help_text='ip'),
        ),
    ]
