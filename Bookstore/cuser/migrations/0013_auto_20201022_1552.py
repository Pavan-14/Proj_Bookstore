# Generated by Django 2.2.15 on 2020-10-22 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuser', '0012_auto_20201022_1141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post_book',
            name='user',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Post_book',
        ),
    ]