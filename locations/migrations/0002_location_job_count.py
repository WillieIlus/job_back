# Generated by Django 4.2.6 on 2024-01-21 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='job_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
