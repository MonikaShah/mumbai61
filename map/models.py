# from django.db import models
# Create your models here.
from django.contrib.gis.db import models

class Ward61OsmBuildings(models.Model):
    geom = models.MultiPolygonField(blank=True, null=True)
    fid = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    osm_id = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    building_t = models.CharField(max_length=80, blank=True, null=True)
    name = models.CharField(max_length=80, blank=True, null=True)
    num_flats = models.BigIntegerField(blank=True, null=True)
    wing = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ward61_osm_buildings'
        
class OsmBuildings29Oct21(models.Model):
    geom = models.MultiPolygonField(blank=True, null=True)  # This field type is a guess.
    fid = models.IntegerField(blank=False, null=False)
    osm_id = models.IntegerField(blank=True, null=True)
    addrstreet = models.CharField(max_length=200, blank=True, null=True)
    building = models.CharField(max_length=80, blank=True, null=True,default = "TestBuilding")
    name = models.CharField(max_length=80, blank=True, null=True, default = "TestName")
    num_flats = models.IntegerField(blank=True, null=True, default =1)
    wings = models.IntegerField(blank=True, null=True,default=1)
    region = models.CharField(max_length=50, blank=True, null=True,default = "TestRegion")

    class Meta:
        managed = False
        db_table = 'osm_buildings_29oct21'