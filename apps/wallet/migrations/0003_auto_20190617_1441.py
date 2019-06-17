# Generated by Django 2.1.2 on 2019-06-17 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_remove_wallet_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to='img/Wallet'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='category',
            field=models.CharField(choices=[('News', 'News'), ('draft', 'draft')], max_length=50),
        ),
    ]
