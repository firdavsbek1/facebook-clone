# Generated by Django 4.2.4 on 2023-08-13 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_story_created_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='expiration_time',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]