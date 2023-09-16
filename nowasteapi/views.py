from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets,serializers

from .serializers import newBuildingDaily,newPrabhagDaily,newRegionDaily,newWardDaily
from .models import BuildingDaily,RegionDaily,PrabhagDaily,WardDaily


class BuildingView(viewsets.ModelViewSet):
    queryset = BuildingDaily.objects.all().order_by('primary_id')
    serializer_class = newBuildingDaily
    # def get_queryset(self,*args, **kwargs):
    #             # selectedTab = self.kwargs.get('tab', None)
    #             queryset = Tracksheet.objects.all().order_by('num_houses_giving_mixwaste')
    #             return queryset

class RegionView(viewsets.ModelViewSet):
    queryset = RegionDaily.objects.all()
    serializer_class = newRegionDaily

class PrabhagView(viewsets.ModelViewSet):
    queryset = PrabhagDaily.objects.all()
    serializer_class = newPrabhagDaily

class WardView(viewsets.ModelViewSet):
    queryset = WardDaily.objects.all()
    serializer_class = newWardDaily