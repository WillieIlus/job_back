# Generated by Django 4.2.6 on 2024-01-01 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_alter_category_options_category_job_count'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('-job_count', 'name'), 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
    ]
