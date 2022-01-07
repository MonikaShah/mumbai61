# from django.db import models
from django.contrib.gis.db import models


# Create your models here.
class WasteSegregationDetails(models.Model):
    track_id = models.IntegerField(blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    building_name = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    num_wings = models.CharField(max_length=100, blank=True, null=True)
    wing_name = models.CharField(max_length=100, blank=True, null=True)
    building_type = models.CharField(max_length=100, blank=True, null=True)
    population = models.CharField(max_length=100, blank=True, null=True)
    num_households_premises = models.CharField(max_length=100, blank=True, null=True)
    num_shops_premises = models.CharField(max_length=100, blank=True, null=True)
    type_waste_generator = models.CharField(max_length=100, blank=True, null=True)
    waste_segregation = models.CharField(max_length=100, blank=True, null=True)
    wet_waste_before_segregation = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    dry_waste_before_segregation = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    hazardous_waste = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    compostable_waste = models.CharField(max_length=100, blank=True, null=True)
    recyclable_waste = models.CharField(max_length=100, blank=True, null=True)
    rejected_waste = models.CharField(max_length=100, blank=True, null=True)
    composting_type = models.CharField(max_length=100, blank=True, null=True)
    compost_bin_by_mcgm = models.CharField(max_length=100, blank=True, null=True)
    date_notice_issued = models.CharField(max_length=100, blank=True, null=True)
    name_number = models.CharField(max_length=100, blank=True, null=True)
    coll_date = models.DateField(blank=True, null=True)
    building_bifurcation = models.CharField(max_length=50, blank=True, null=True)
    admin_ward = models.CharField(max_length=50, blank=True, null=True)
    councillor_ward = models.CharField(max_length=50, blank=True, null=True)
    ward = models.CharField(default = '61',max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'waste_segregation_details'

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

