from django.db import models

# Create your models here.

class BuildingDaily(models.Model):
    id =models.IntegerField(primary_key=True)
    primary_id = models.DecimalField(max_digits=10, decimal_places=0)
    parent_id = models.DecimalField(max_digits=10, decimal_places=0)
    dry_waste = models.DecimalField(max_digits=20, decimal_places=0)
    wet_waste = models.DecimalField(max_digits=20, decimal_places=0)
    total_waste = models.DecimalField(max_digits=20, decimal_places=0)
    population = models.IntegerField()
    weight = models.DecimalField(max_digits=20, decimal_places=0)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'building_daily'

class BuildingMonthly(models.Model):
    primary_id = models.DecimalField(max_digits=10, decimal_places=0)
    parent_id = models.DecimalField(max_digits=10, decimal_places=0)
    dry_waste = models.DecimalField(max_digits=20, decimal_places=0)
    wet_waste = models.DecimalField(max_digits=20, decimal_places=0)
    total_waste = models.DecimalField(max_digits=20, decimal_places=0)
    population = models.IntegerField()
    weight = models.DecimalField(max_digits=20, decimal_places=0)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'building_monthly'
class BuildingYearly(models.Model):
    primary_id = models.DecimalField(max_digits=10, decimal_places=0)
    parent_id = models.DecimalField(max_digits=10, decimal_places=0)
    dry_waste = models.DecimalField(max_digits=20, decimal_places=0)
    wet_waste = models.DecimalField(max_digits=20, decimal_places=0)
    total_waste = models.DecimalField(max_digits=20, decimal_places=0)
    population = models.IntegerField()
    weight = models.DecimalField(max_digits=20, decimal_places=0)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'building_yearly'
# region data
class RegionDaily(models.Model):
    primary_id = models.DecimalField(max_digits=10, decimal_places=0)
    parent_id = models.DecimalField(max_digits=10, decimal_places=0)
    dry_waste = models.DecimalField(max_digits=20, decimal_places=0)
    wet_waste = models.DecimalField(max_digits=20, decimal_places=0)
    total_waste = models.DecimalField(max_digits=20, decimal_places=0)
    population = models.IntegerField()
    weight = models.DecimalField(max_digits=20, decimal_places=0)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'region_daily'

class RegionMonthly(models.Model):
    primary_id = models.DecimalField(max_digits=10, decimal_places=0)
    parent_id = models.DecimalField(max_digits=10, decimal_places=0)
    dry_waste = models.DecimalField(max_digits=20, decimal_places=0)
    wet_waste = models.DecimalField(max_digits=20, decimal_places=0)
    total_waste = models.DecimalField(max_digits=20, decimal_places=0)
    population = models.IntegerField()
    weight = models.DecimalField(max_digits=20, decimal_places=0)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'region_monthly'

class RegionYearly(models.Model):
    primary_id = models.DecimalField(max_digits=10, decimal_places=0)
    parent_id = models.DecimalField(max_digits=10, decimal_places=0)
    dry_waste = models.DecimalField(max_digits=20, decimal_places=0)
    wet_waste = models.DecimalField(max_digits=20, decimal_places=0)
    total_waste = models.DecimalField(max_digits=20, decimal_places=0)
    population = models.IntegerField()
    weight = models.DecimalField(max_digits=20, decimal_places=0)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'region_yearly'
    
    # Prabhag data
class PrabhagDaily(models.Model):
    primary_id = models.DecimalField(max_digits=10, decimal_places=0)
    parent_id = models.DecimalField(max_digits=10, decimal_places=0)
    dry_waste = models.DecimalField(max_digits=20, decimal_places=0)
    wet_waste = models.DecimalField(max_digits=20, decimal_places=0)
    total_waste = models.DecimalField(max_digits=20, decimal_places=0)
    population = models.IntegerField()
    weight = models.DecimalField(max_digits=20, decimal_places=0)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'prabhag_daily'

class PrabhagMonthly(models.Model):
    primary_id = models.DecimalField(max_digits=10, decimal_places=0)
    parent_id = models.DecimalField(max_digits=10, decimal_places=0)
    dry_waste = models.DecimalField(max_digits=20, decimal_places=0)
    wet_waste = models.DecimalField(max_digits=20, decimal_places=0)
    total_waste = models.DecimalField(max_digits=20, decimal_places=0)
    population = models.IntegerField()
    weight = models.DecimalField(max_digits=20, decimal_places=0)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'prabhag_monthly'
class PrabhagYearly(models.Model):
    primary_id = models.DecimalField(max_digits=10, decimal_places=0)
    parent_id = models.DecimalField(max_digits=10, decimal_places=0)
    dry_waste = models.DecimalField(max_digits=20, decimal_places=0)
    wet_waste = models.DecimalField(max_digits=20, decimal_places=0)
    total_waste = models.DecimalField(max_digits=20, decimal_places=0)
    population = models.IntegerField()
    weight = models.DecimalField(max_digits=20, decimal_places=0)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'prabhag_yearly'

# ward data 
class WardDaily(models.Model):
    primary_id = models.DecimalField(max_digits=10, decimal_places=0)
    parent_id = models.DecimalField(max_digits=10, decimal_places=0)
    dry_waste = models.DecimalField(max_digits=20, decimal_places=0)
    wet_waste = models.DecimalField(max_digits=20, decimal_places=0)
    total_waste = models.DecimalField(max_digits=20, decimal_places=0)
    population = models.IntegerField()
    weight = models.DecimalField(max_digits=20, decimal_places=0)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'ward_daily'

class WardMonthly(models.Model):
    primary_id = models.DecimalField(max_digits=10, decimal_places=0)
    parent_id = models.DecimalField(max_digits=10, decimal_places=0)
    dry_waste = models.DecimalField(max_digits=20, decimal_places=0)
    wet_waste = models.DecimalField(max_digits=20, decimal_places=0)
    total_waste = models.DecimalField(max_digits=20, decimal_places=0)
    population = models.IntegerField()
    weight = models.DecimalField(max_digits=20, decimal_places=0)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'ward_monthly'
class WardYearly(models.Model):
    primary_id = models.DecimalField(max_digits=10, decimal_places=0)
    parent_id = models.DecimalField(max_digits=10, decimal_places=0)
    dry_waste = models.DecimalField(max_digits=20, decimal_places=0)
    wet_waste = models.DecimalField(max_digits=20, decimal_places=0)
    total_waste = models.DecimalField(max_digits=20, decimal_places=0)
    population = models.IntegerField()
    weight = models.DecimalField(max_digits=20, decimal_places=0)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'ward_yearly'
