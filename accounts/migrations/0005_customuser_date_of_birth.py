# Generated by Django 4.2.18 on 2025-02-10 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customuser_address_customuser_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
