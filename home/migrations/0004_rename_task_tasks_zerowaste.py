# Generated by Django 4.1.7 on 2023-07-05 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zerowaste', '0006_data_form_compost_data_username_and_more'),
        ('home', '0003_task'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Task',
            new_name='tasks_zerowaste',
        ),
    ]