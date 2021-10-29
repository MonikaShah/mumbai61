from django.shortcuts import render
from zerowaste.models import OsmBuildings29Oct21

# Create your views here.
# from swk.HelloAnalytics import *

def Map(request):
   data = OsmBuildings29Oct21.objects.all
   context = {
        'data':data,
        #'Visitor_count': recd_response
        }  
   
   return render(request, "map/map.html",context)

   #return render(request,"map/map.html")