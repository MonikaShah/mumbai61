# Generated by Django 4.1.3 on 2023-07-28 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0001_initial'),
        ('zerowaste', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks_zerowaste',
            name='zerowaste_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zerowaste.authuser'),
        ),
    ]
