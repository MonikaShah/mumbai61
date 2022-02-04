from django.shortcuts import render
# from zerowaste.models import OsmBuildings29Oct21
from django.core.serializers import serialize
from .models import Ward61BuildingsOsm2Nov2021,MumbaiPrabhagBoundaries3Jan2022V2,MumbaiWardBoundary2Jan2022,DistinctGeomSacNoMumbai,MumbaiBuildingsWardPrabhagwise17Jan #,Ward61OsmBuildings,
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
   print("in map")
   if is_ajax(request=request):
      requestvar = request.get_full_path()
      print(requestvar)
        # if(requestvar!=null):
        # docinfo = []
        # docinfo1 =[]
        
        # 

        # if(requestvar.find('name1')):
      if "name1" in requestvar:
   # if request.is_ajax():
         prabhag = request.GET['name1']
         data= list(MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(prabhag_no=prabhag))
         geojson=serialize('geojson',data)
         return JsonResponse(geojson, safe=False)
      
      elif "name2" in requestvar:
         sel_ward = request.GET['name2']
         prabhag_list = list(MumbaiPrabhagBoundaries3Jan2022V2.objects.filter(ward_id=sel_ward).values('prabhag_no','ward_name','ward_id'))
         print(prabhag_list)
         return JsonResponse(prabhag_list, safe=False)
      else:
         selected_field1 = request.GET['name']
         docinfo1 = list(MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(sac_number=selected_field1).values('sac_number','prop_add','building_type','building_name','village','num_flat','region','num_shops','wing_name','prabhag_no','ward_name_field','address','validity'))
         jsondata2 =docinfo1[0]
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
      # print(request.user.is_anonymous)
      geojson=[]
      ward=[]
      ward_id=[]
      ward_list=list(MumbaiWardBoundary2Jan2022.objects.values('ward_id','ward_name_field'))
      # print(ward_list)
      prabhag_mumbai=list(MumbaiPrabhagBoundaries3Jan2022V2.objects.values('prabhag_no'))
      prabhag_list=[]
      prabhag=[]
      data = []
      if (request.user is not None) and (request.user.is_anonymous is False):
         ward = request.user.Ward
         prabhag = request.user.prabhag
         ward_id = list(MumbaiWardBoundary2Jan2022.objects.filter(ward_name_field= ward))
         sel_ward = ward_id[0].ward_id
         prabhag_list = list(MumbaiPrabhagBoundaries3Jan2022V2.objects.filter(ward_id=sel_ward))
         if  request.user.groups.filter(name="prabhagEditor").exists():
            data= list(MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(prabhag_no=prabhag))
            
         elif  request.user.groups.filter(name="wardEditor").exists():
            data= list(MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(ward_id_2=sel_ward))
         geojson=serialize('geojson',data)
         return render(request,"map/map_new.html",{ 'ward':ward,'prabhag_list':prabhag_list,'prabhag_mumbai':prabhag_mumbai,'ward_list':ward_list,'prabhag':prabhag,'geojson':geojson})
      # obj=Ward61BuildingsOsm2Nov2021.objects.all()
      # kwest  =  KwestBuildingUpdated.objects.all()
      # kwestgeojson =  serialize('geojson',kwest)
#  print(geojson)
#  context = 
   return render(request,"map/map_new.html",{ 'ward':ward,'prabhag_list':prabhag_list,'ward_list':ward_list,'prabhag':prabhag,'geojson':geojson,'prabhag_mumbai':prabhag_mumbai})