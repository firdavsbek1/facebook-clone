# Generated by Django 4.2.4 on 2023-08-09 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_customuser_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='last_activity',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
