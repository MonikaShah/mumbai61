from rest_framework import serializers

from .models import BuildingDaily,BuildingMonthly,BuildingYearly, RegionDaily,RegionMonthly,RegionYearly,PrabhagDaily,PrabhagMonthly,PrabhagYearly,WardDaily,WardMonthly,WardYearly

class newBuildingDaily(serializers.HyperlinkedModelSerializer):
    primary_id = serializers.CharField(source='id')
    class Meta:
        model = BuildingDaily
        fields = ("id",
        "primary_id",
        "parent_id",
        "dry_waste",
        "wet_waste",
        "total_waste",
        "population",
        "weight",
        "date",
        )

class newPrabhagDaily(serializers.HyperlinkedModelSerializer):
    primary_id = serializers.CharField(source='primary_id_id')
    class Meta:
        model = PrabhagDaily
        fields = ( "primary_id",
        "parent_id",
        "dry_waste",
        "wet_waste",
        "total_waste",
        "population",
        "weight",
        "date",
        )
class newRegionDaily(serializers.HyperlinkedModelSerializer):
    primary_id = serializers.CharField(source='primary_id_id')
    class Meta:
        model = RegionDaily
        fields = ( "primary_id",
        "parent_id",
        "dry_waste",
        "wet_waste",
        "total_waste",
        "population",
        "weight",
        "date",
        )
class newWardDaily(serializers.HyperlinkedModelSerializer):
    primary_id = serializers.CharField(source='primary_id_id')
    class Meta:
        model = WardDaily
        fields = ( "primary_id",
        "parent_id",
        "dry_waste",
        "wet_waste",
        "total_waste",
        "population",
        "weight",
        "date",
        )