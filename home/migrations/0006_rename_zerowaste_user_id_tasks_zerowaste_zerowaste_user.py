# Generated by Django 4.1.7 on 2023-07-05 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_rename_zerowaste_user_tasks_zerowaste_zerowaste_user_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tasks_zerowaste',
            old_name='zerowaste_user_id',
            new_name='zerowaste_user',
        ),
    ]
