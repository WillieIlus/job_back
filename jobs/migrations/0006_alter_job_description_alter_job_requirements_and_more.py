# Generated by Django 4.2.6 on 2024-01-07 19:55

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_alter_job_requirements_alter_job_responsibilities'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='description',
            field=markdownx.models.MarkdownxField(blank=True, max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='requirements',
            field=markdownx.models.MarkdownxField(blank=True, max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='responsibilities',
            field=markdownx.models.MarkdownxField(blank=True, max_length=4000, null=True),
        ),
    ]
