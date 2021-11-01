from django.shortcuts import render
# from zerowaste.models import OsmBuildings29Oct21
from django.core.serializers import serialize
from .models import Ward61OsmBuildings,OsmBuildings29Oct21

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
     # obj = Ward61OsmBuildings.objects.all()
    obj = OsmBuildings29Oct21.objects.all()
    geojson = serialize('geojson',obj)
    context = {'geojson':geojson}
    return render(req,"map/map.html",context)