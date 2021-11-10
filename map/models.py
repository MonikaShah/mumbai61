# from django.db import models
# Create your models here.
from django.contrib.gis.db import models


class Ward61OsmBuildings(models.Model):
    geom = models.MultiPolygonField(blank=True, null=True)
    fid = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    osm_id = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    building = models.CharField(max_length=80, blank=True, null=True)
    name = models.CharField(max_length=80, blank=True, null=True)
    num_flats = models.BigIntegerField(blank=True, null=True)
    wings = models.CharField(max_length=10, blank=True, null=True)
    addrstreet = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'osm_buildings_29oct21'

class Ward61BuildingsOsm2Nov2021(models.Model):
    geom = models.MultiPolygonField(blank=True, null=True)
    osm_id = models.IntegerField()
    name = models.CharField(max_length=97, blank=True, null=True)
    addrstreet = models.CharField(max_length=91, blank=True, null=True)
    building = models.CharField(max_length=80, blank=True, null=True)
    roofmateri = models.CharField(max_length=80, blank=True, null=True)
    osmward = models.CharField(max_length=100, blank=True, null=True)
    num_flat = models.IntegerField(blank=True, null=True)
    num_shops = models.IntegerField(blank=True, null=True)
    wing = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ward61_buildings_osm_2nov2021'

# class Ward61OsmBuildings1Nov21(models.Model):
#     geom = models.MultiPolygonField(blank=True, null=True)
#     ward = models.CharField(max_length=254, blank=True, null=True)
#     fid_2 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
#     osm_id = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
#     name = models.CharField(max_length=254, blank=True, null=True)
#     addrstreet = models.CharField(max_length=254, blank=True, null=True)
#     building = models.CharField(max_length=254, blank=True, null=True)
#     num_flats = models.IntegerField(blank=True, null=True)
#     wings = models.CharField(max_length=10, blank=True, null=True)
#     region = models.CharField(max_length=10, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'ward61_osm_buildings_1nov21'

# class Ward61OsmBuildings1Nov21(models.Model):
#     id = models.IntegerField(primary_key=True)
#     geom = models.MultiPolygonField(blank=True, null=True)
#     ward = models.CharField(max_length=254, blank=True, null=True)
#     fid_2 = models.IntegerField(blank=True, null=True)
#     osm_id = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
#     name = models.CharField(max_length=254, blank=True, null=True)
#     addrstreet = models.CharField(max_length=254, blank=True, null=True)
#     building = models.CharField(max_length=254, blank=True, null=True)
#     num_flats = models.IntegerField(blank=True, null=True)
#     wings = models.CharField(max_length=10, blank=True, null=True)
#     region = models.CharField(max_length=10, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'ward61_osm_buildings_1nov21'


# class OsmBuildings1Nov21(models.Model):
#     id = models.IntegerField(primary_key=True)
#     geom = models.MultiPolygonField(blank=True, null=True)
#     ward = models.CharField(max_length=254, blank=True, null=True)
#     fid_2 = models.IntegerField(blank=True, null=True)
#     osm_id = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
#     name = models.CharField(max_length=254, blank=True, null=True)
#     addrstreet = models.CharField(max_length=254, blank=True, null=True)
#     building = models.CharField(max_length=254, blank=True, null=True)
#     num_flats = models.IntegerField(blank=True, null=True)
#     wings = models.CharField(max_length=10, blank=True, null=True)
#     region = models.CharField(max_length=10, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'osm_buildings_1nov21'


# class Buildings2Nov(models.Model):
#     geom = models.MultiPolygonField(blank=True, null=True)
#     ward = models.CharField(max_length=254, blank=True, null=True)
#     fid_2 = models.IntegerField(blank=True, null=True)
#     osm_id = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
#     name = models.CharField(max_length=254, blank=True, null=True)
#     addrstreet = models.CharField(max_length=254, blank=True, null=True)
#     building = models.CharField(max_length=254, blank=True, null=True)
#     num_flats = models.IntegerField(blank=True, null=True)
#     wings = models.CharField(max_length=10, blank=True, null=True)
#     region = models.CharField(max_length=10, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'buildings_2nov'