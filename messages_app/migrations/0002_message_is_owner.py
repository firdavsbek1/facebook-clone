# Generated by Django 4.2.4 on 2023-08-14 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messages_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_owner',
            field=models.BooleanField(default=False),
        ),
    ]