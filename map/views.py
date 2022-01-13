from django.shortcuts import render
# from zerowaste.models import OsmBuildings29Oct21
from django.core.serializers import serialize
from .models import Ward61BuildingsOsm2Nov2021,AllPropDataKwest,KwestBldngSacRelation,KwestBuildingUpdated #,Ward61OsmBuildings,
from django.http import JsonResponse
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
def is_ajax(request):
   return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
def Map(request):
   print(request)
   if is_ajax(request=request):

   # if request.is_ajax():
      selected_field1 = request.GET['name']
      docinfo1 = list(KwestBuildingUpdated.objects.defer('geom').filter(sac_no=selected_field1).values('id','sac_no','section','building_type','building_name','prop_blng_add','fda','address','metered_un','prop_tax_30_3_20','yearly_demand','despute','remarks','village','num_flat','region','num_shops','wing_name'))
      jsondata2 =docinfo1[0]
      print(jsondata2)
      return JsonResponse(docinfo1[0])
      
   
      # elif "name" in requestvar:
      #    selected_field = request.GET['name']
      #    print(selected_field)
      #    docinfo = list(SwkAttendants.objects.filter(zone_name=selected_field).values()); 
      #    print("doc info is " ,docinfo)
      #    jsondata2 =docinfo[0]
      #    # field=docinfo[0]["zone_id"]
      #    # print(field)
      #    # docinfo1 = list(SwkAttendants.objects.filter(zone_id=field).values()); 
      #    # jsondata2=docinfo1[0]
      #    # print("docinfo 0 is ",docinfo[0])
      #    return JsonResponse(jsondata2)
       
   #  obj = Ward61OsmBuildings.objects.all()
   if request.method == 'GET':

      obj=Ward61BuildingsOsm2Nov2021.objects.all()
      kwest  =  KwestBuildingUpdated.objects.all()
      geojson=serialize('geojson',obj)
      kwestgeojson =  serialize('geojson',kwest)
#  print(geojson)
#  context = 
   return render(request,"map/map_new.html",{'geojson':geojson,'kwestgeojson':kwestgeojson})