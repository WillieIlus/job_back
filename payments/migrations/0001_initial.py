# Generated by Django 4.2.6 on 2023-12-26 18:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MpesaPaymentResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_request_id', models.CharField(max_length=100)),
                ('checkout_request_id', models.CharField(max_length=100)),
                ('response_code', models.CharField(max_length=10)),
                ('response_description', models.CharField(max_length=200)),
                ('customer_message', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_no', models.CharField(default=uuid.uuid4, max_length=50, unique=True)),
                ('phone_number', models.IntegerField()),
                ('checkout_request_id', models.CharField(max_length=200)),
                ('reference', models.CharField(blank=True, max_length=40)),
                ('description', models.TextField(blank=True, null=True)),
                ('amount', models.CharField(max_length=10)),
                ('status', models.CharField(choices=[(1, 'Pending'), (0, 'Complete')], default=1, max_length=15)),
                ('receipt_no', models.CharField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ip', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]