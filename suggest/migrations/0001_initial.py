# Generated by Django 2.2.2 on 2020-10-21 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Suggest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(help_text='建议内容', max_length=500)),
                ('email', models.EmailField(help_text='用户 email', max_length=254)),
                ('platform', models.CharField(help_text='提交平台：android/ios/browser 等', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
