# Generated by Django 5.0.13 on 2025-04-23 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FlightApp', '0003_airlinelog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pilot',
            name='total_flight_hours',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
