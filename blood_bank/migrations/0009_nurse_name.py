# Generated by Django 4.0.3 on 2022-09-01 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood_bank', '0008_donator_name_alter_donator_birth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='nurse',
            name='name',
            field=models.CharField(default=None, max_length=250),
            preserve_default=False,
        ),
    ]
