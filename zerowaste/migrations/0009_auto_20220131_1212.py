# Generated by Django 2.2.12 on 2022-01-31 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zerowaste', '0008_user_area_user_designation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='area',
            field=models.CharField(choices=[('Select', 'none'), ('Ward', 'Ward'), ('Prabhag', 'Prabhag')], default='none', max_length=9),
        ),
    ]
