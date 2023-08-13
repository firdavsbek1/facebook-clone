# Generated by Django 4.2.4 on 2023-08-12 17:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_friendlist_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendlist',
            name='friends',
            field=models.ManyToManyField(related_name='friends', to=settings.AUTH_USER_MODEL),
        ),
    ]
