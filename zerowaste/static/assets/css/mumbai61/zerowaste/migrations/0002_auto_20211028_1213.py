# Generated by Django 3.0 on 2021-10-28 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zerowaste', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='burnable_waste_in_kg',
        ),
        migrations.RemoveField(
            model_name='report',
            name='kitchen_waste_in_kg',
        ),
        migrations.RemoveField(
            model_name='report',
            name='landfill_inside_house',
        ),
        migrations.RemoveField(
            model_name='report',
            name='landfill_surrounding',
        ),
        migrations.RemoveField(
            model_name='report',
            name='zone_name',
        ),
        migrations.AddField(
            model_name='report',
            name='compostable_waste',
            field=models.FloatField(blank=True, db_column='compostable_waste', null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='dry_waste_bf',
            field=models.FloatField(blank=True, db_column='dry_waste_bf', null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='hazardous_waste',
            field=models.FloatField(blank=True, db_column='hazardous_waste', null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='region_name',
            field=models.CharField(default='region A', max_length=100),
        ),
        migrations.AddField(
            model_name='report',
            name='wet_waste_bf',
            field=models.FloatField(blank=True, db_column='wet_waste_bf', null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='recyclable_waste',
            field=models.FloatField(blank=True, db_column='recyclable_waste', null=True),
        ),
    ]