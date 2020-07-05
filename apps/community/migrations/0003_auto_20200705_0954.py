# Generated by Django 2.2.2 on 2020-07-05 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_auto_20200705_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='status',
            field=models.CharField(choices=[('unchecked', 'unchecked'), ('submitted', 'submitted'), ('deposited', 'deposited'), ('community congress', 'community congress'), ('decision congress', 'decision congress'), ('passed', 'passed'), ('declined', 'declined'), ('timeout', 'timeout')], default='unchecked', help_text='提案状态', max_length=30),
        ),
    ]
