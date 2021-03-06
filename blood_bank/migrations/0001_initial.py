# Generated by Django 4.0.3 on 2022-03-24 20:46

import cpf_field.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=50)),
                ('neighborhood', models.CharField(max_length=50)),
                ('number', models.IntegerField(null=True)),
                ('reference_point', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CollectionBags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_bag', models.SlugField(default='123', max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('local', models.CharField(max_length=100)),
                ('real_weight', models.FloatField()),
                ('temperature', models.FloatField()),
                ('entry_time', models.DateTimeField()),
                ('exit_time', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Tubes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_tube', models.SlugField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telephone1', models.CharField(max_length=11)),
                ('telephone2', models.CharField(max_length=11, null=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blood_bank.address')),
            ],
        ),
        migrations.CreateModel(
            name='Exams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('state_exam', models.CharField(choices=[('y', 'exam valid'), ('n', 'exam not valid'), ('w', 'waiting exam result')], max_length=3)),
                ('donation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blood_bank.donation')),
            ],
        ),
        migrations.CreateModel(
            name='Donator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_type', models.CharField(choices=[('a+', 'A positive'), ('a-', 'A negative'), ('b+', 'B positive'), ('b-', 'B negative'), ('ab+', 'AB positive'), ('ab-', 'AB negative'), ('o+', 'O positive'), ('o-', 'O negative')], max_length=3)),
                ('telephone1', models.CharField(max_length=11)),
                ('telephone2', models.CharField(max_length=11, null=True)),
                ('birth_date', models.DateField()),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blood_bank.address')),
            ],
        ),
        migrations.AddField(
            model_name='donation',
            name='donator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blood_bank.donator'),
        ),
        migrations.AddField(
            model_name='donation',
            name='nurse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blood_bank.nurse'),
        ),
        migrations.AddField(
            model_name='donation',
            name='serial_number_collection_bag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blood_bank.collectionbags'),
        ),
        migrations.AddField(
            model_name='donation',
            name='test_tube',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blood_bank.tubes'),
        ),
        migrations.CreateModel(
            name='Allergies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('res', 'respiratory allergies'), ('ski', 'skin allergies'), ('eye', 'eye allergies'), ('foo', 'food allergies'), ('dru', 'drug allergies')], max_length=3)),
                ('subject', models.CharField(max_length=30)),
                ('donator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blood_bank.donator')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=250, unique=True)),
                ('cpf', cpf_field.models.CPFField(max_length=11)),
                ('user_type', models.CharField(choices=[('don', 'donator'), ('nur', 'nurse'), ('adm', 'admin')], max_length=3)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
