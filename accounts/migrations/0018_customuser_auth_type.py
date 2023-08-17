# Generated by Django 4.2.4 on 2023-08-17 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_codeverification'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='auth_type',
            field=models.CharField(choices=[('EMAIL', 'via_email'), ('PHONE', 'via_phone')], default='EMAIL', max_length=15),
        ),
    ]
