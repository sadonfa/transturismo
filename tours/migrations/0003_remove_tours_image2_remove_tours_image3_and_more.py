# Generated by Django 5.0.7 on 2024-07-24 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0002_alter_tours_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tours',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='tours',
            name='image3',
        ),
        migrations.RemoveField(
            model_name='tours',
            name='image4',
        ),
    ]