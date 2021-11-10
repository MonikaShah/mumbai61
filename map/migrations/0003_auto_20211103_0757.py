# Generated by Django 3.0 on 2021-11-03 07:57

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0002_buildings2nov'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ward61BuildingsOsm2Nov2021',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
                ('osm_id', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('name', models.CharField(blank=True, max_length=97, null=True)),
                ('addrstreet', models.CharField(blank=True, max_length=91, null=True)),
                ('building', models.CharField(blank=True, max_length=80, null=True)),
                ('roofmateri', models.CharField(blank=True, max_length=80, null=True)),
                ('osmward', models.CharField(blank=True, max_length=100, null=True)),
                ('num_flat', models.IntegerField(blank=True, null=True)),
                ('num_shops', models.IntegerField(blank=True, null=True)),
                ('wing', models.CharField(blank=True, max_length=100, null=True)),
                ('region', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'ward61_buildings_osm_2nov2021',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Buildings2Nov',
        ),
        migrations.DeleteModel(
            name='OsmBuildings1Nov21',
        ),
        migrations.DeleteModel(
            name='Ward61OsmBuildings1Nov21',
        ),
        migrations.AlterModelTable(
            name='ward61osmbuildings',
            table='osm_buildings_29oct21',
        ),
    ]
