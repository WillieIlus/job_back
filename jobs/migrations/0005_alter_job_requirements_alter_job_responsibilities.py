# Generated by Django 4.2.6 on 2024-01-01 10:16

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_job_last_clicked_at_job_last_viewed_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='requirements',
            field=markdownx.models.MarkdownxField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='responsibilities',
            field=markdownx.models.MarkdownxField(blank=True, max_length=2000, null=True),
        ),
    ]
