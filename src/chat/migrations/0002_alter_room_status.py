# Generated by Django 4.2.11 on 2024-03-22 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='status',
            field=models.CharField(choices=[('closed', 'Closed'), ('active', 'Active'), ('waiting', 'Waiting')], default='waiting', max_length=20),
        ),
    ]