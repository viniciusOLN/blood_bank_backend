# Generated by Django 4.0.3 on 2022-09-15 23:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blood_bank', '0012_alter_myuser_birth_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donator',
            name='is_active',
        ),
    ]