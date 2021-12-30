from django.shortcuts import render
# from zerowaste.models import OsmBuildings29Oct21
from django.core.serializers import serialize
from .models import Ward61BuildingsOsm2Nov2021,AllPropDataKwest,KwestBldngSacRelation #,Ward61OsmBuildings,

# Create your views here.
# from swk.HelloAnalytics import *

# def Map(request):
#    data = OsmBuildings29Oct21.objects.all
#    context = {
#         'data':data,
#         #'Visitor_count': recd_response
#         }  
   
#    return render(request, "map/map.html",context)

   #return render(request,"map/map.html")

def Map(req):
   #  obj = Ward61OsmBuildings.objects.all()
    obj=Ward61BuildingsOsm2Nov2021.objects.all()
    kwest  =  AllPropDataKwest.objects.all()
    geojson=serialize('geojson',obj)
    kwestgeojson =  serialize('geojson',kwest)
   #  print(geojson)
   #  context = 
    return render(req,"map/map.html",{'geojson':geojson,'kwestgeojson':kwestgeojson})