# Generated by Django 2.2.15 on 2020-10-06 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuser', '0003_auto_20201001_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_verified',
            field=models.BooleanField(default=False, verbose_name='Email Verified'),
        ),
    ]