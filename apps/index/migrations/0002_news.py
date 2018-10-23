# Generated by Django 2.1.2 on 2018-10-22 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Community Updates', 'Community Updates'), ('AMA Sessions', 'AMA Sessions'), ('Media Reports', 'Media Reports')], max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('update_time', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
