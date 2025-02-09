# Generated by Django 5.0.6 on 2025-02-02 13:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_doctor_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientParent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
                ('id_number', models.CharField(default='', max_length=30)),
                ('contact_phone_number', models.CharField(default='', max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='patient',
            name='email',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='id_number',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='last_name',
        ),
        migrations.AddField(
            model_name='patient',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='patient',
            name='parent',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='patient_parents', to='users.patientparent'),
        ),
    ]
