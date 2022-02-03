# from django.db import models
# Create your models here.
from django.contrib.gis.db import models


# class Ward61OsmBuildings(models.Model):
#     geom = models.MultiPolygonField(blank=True, null=True)
#     fid = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
#     osm_id = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
#     building = models.CharField(max_length=80, blank=True, null=True)
#     name = models.CharField(max_length=80, blank=True, null=True)
#     num_flats = models.BigIntegerField(blank=True, null=True)
#     wings = models.CharField(max_length=10, blank=True, null=True)
#     addrstreet = models.CharField(max_length=100, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'osm_buildings_29oct21'
class MumbaiWardBoundary2Jan2022(models.Model):
    geom = models.MultiPolygonField(blank=True, null=True)
    fid = models.IntegerField(blank=True, null=True)
    district = models.CharField(max_length=254, blank=True, null=True)
    ward_id = models.CharField(max_length=254,unique=True, blank=True, null=True)
    ward_name_field = models.CharField(db_column='ward_name_', max_length=254, blank=True, null=True)  # Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'mumbai_ward_boundary_2Jan2022'
        
        ordering = ["ward_name_field"]
    def __str__(self):
        return self.ward_name_field
class MumbaiPrabhagBoundaries3Jan2022V2(models.Model):
    geom = models.MultiPolygonField(blank=True, null=True)
    fid = models.IntegerField(blank=True, null=True)
    prabhag_no = models.CharField(max_length=254,unique=True, blank=True, null=True)
    ward_name = models.CharField(max_length=254, blank=True, null=True)
    ward_id = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Mumbai_Prabhag_Boundaries_3Jan2022V2'
        ordering = ["prabhag_no"]
    def __str__(self):
        return self.prabhag_no

class Ward61BuildingsOsm2Nov2021(models.Model):
    geom = models.MultiPolygonField(blank=True, null=True)
    osm_id = models.IntegerField()
    building_name = models.CharField(max_length=97, blank=True, null=True)
    addrstreet = models.CharField(max_length=91, blank=True, null=True)
    building_type = models.CharField(max_length=80, blank=True, null=True)
    roofmateri = models.CharField(max_length=80, blank=True, null=True)
    osmward = models.CharField(max_length=100, blank=True, null=True)
    num_flat = models.IntegerField(blank=True, null=True,default=1)
    num_shops = models.IntegerField(blank=True, null=True,default=0)
    num_floors = models.IntegerField(blank=True, null=True,default=1)
    wing_name = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    councillor_ward = models.CharField(max_length=100, default='ward61')
    admin_ward = models.CharField(max_length=100, default='ward-KWest')

    class Meta:
        managed = False
        db_table = 'ward61_buildings_osm_2nov2021'
    def __str__(self):        
        return self.building_name
class DistinctGeomSacNoMumbai(models.Model):
    geom = models.PointField(blank=True, null=True)
    wkt = models.CharField(max_length=255, blank=True, null=True)
    building_i = models.CharField(max_length=255, blank=True, null=True)
    sac_number = models.CharField(max_length=255, blank=True, null=True)
    mcgm_usern = models.CharField(max_length=255, blank=True, null=True)
    mcgm_updat = models.CharField(max_length=255, blank=True, null=True)
    sac_type = models.CharField(max_length=255, blank=True, null=True)
    wing_name = models.CharField(max_length=255, blank=True, null=True)
    num_flat = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    num_shops = models.CharField(max_length=255, blank=True, null=True)
    num_floors = models.CharField(max_length=255, blank=True, null=True)
    building_name = models.CharField(max_length=255, blank=True, null=True)
    building_type = models.CharField(max_length=255, blank=True, null=True)
    village = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'distinct_geom_sac_no_mumbai'








class MumbaiBuildingsWardPrabhagwise17Jan(models.Model):
    geom = models.MultiPointField(blank=True, null=True)
    wkt = models.CharField(max_length=255, blank=True, null=True)
    building_i = models.CharField(max_length=255, blank=True, null=True)
    sac_number = models.CharField(max_length=255, blank=True, null=True)
    mcgm_usern = models.CharField(max_length=255, blank=True, null=True)
    mcgm_updat = models.CharField(max_length=255, blank=True, null=True)
    sac_type = models.CharField(max_length=255, blank=True, null=True)
    wing_name = models.CharField(max_length=255, blank=True, null=True)
    num_flat = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    num_shops = models.CharField(max_length=255, blank=True, null=True)
    num_floors = models.CharField(max_length=255, blank=True, null=True)
    building_name = models.CharField(max_length=255, blank=True, null=True)
    building_type = models.CharField(max_length=255, blank=True, null=True)
    village = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    before_geo = models.CharField(max_length=254, blank=True, null=True)
    id1 = models.BigIntegerField(blank=True, null=True)
    prabhag_no = models.CharField(max_length=254, blank=True, null=True)
    fid = models.IntegerField(blank=True, null=True)
    district = models.CharField(max_length=254, blank=True, null=True)
    ward_id_2 = models.CharField(max_length=254, blank=True, null=True)
    ward_name_field = models.CharField(db_column='ward_name_', max_length=254, blank=True, null=True)  # Field renamed because it ended with '_'.
    description = models.CharField(max_length=255, blank=True, null=True)
    prop_add = models.CharField(max_length=255, blank=True, null=True)
    validity = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mumbai_buildings_ward_prabhagwise_17jan'




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