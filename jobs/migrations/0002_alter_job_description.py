# Generated by Django 4.2.6 on 2023-12-27 19:59

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='description',
            field=markdownx.models.MarkdownxField(blank=True, max_length=2000, null=True),
        ),
    ]
