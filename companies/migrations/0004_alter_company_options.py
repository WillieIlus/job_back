# Generated by Django 4.2.6 on 2024-01-30 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_company_job_count'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ('-job_count', '-created_at', '-updated_at', 'name'), 'verbose_name': 'Company', 'verbose_name_plural': 'Companies'},
        ),
    ]
