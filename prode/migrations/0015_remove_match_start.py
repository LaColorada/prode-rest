# Generated by Django 4.0.5 on 2022-06-21 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prode', '0014_match_start_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='start',
        ),
    ]
