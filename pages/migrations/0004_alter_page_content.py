# Generated by Django 5.0.7 on 2024-08-12 13:32

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_alter_page_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Contenido'),
        ),
    ]