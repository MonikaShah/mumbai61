from django.shortcuts import render
# from zerowaste.models import OsmBuildings29Oct21
from django.core.serializers import serialize
from .models import Ward61BuildingsOsm2Nov2021,MumbaiPrabhagBoundaries3Jan2022V2,MumbaiWardBoundary2Jan2022,DistinctGeomSacNoMumbai,MumbaiBuildingsWardPrabhagwise17Jan #,Ward61OsmBuildings,
from zerowaste.models import BuildingsWard9April22,WasteSegregationDetailsRevised2March22#,BuildingsWardWise4March
from django.http import JsonResponse
from datetime import date
from datetime import timedelta
 
# Get today's date

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
   
   data_buildings_132 = list(MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(prabhag_no='132'))
   data_buildings_122 = list(MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(prabhag_no='122'))
   # data_buildings_122_1=['SX1204540180000','SX1204950160000']
   # print(data_buildings_132[0])
   data_buildings_122_1 = list(MumbaiBuildingsWardPrabhagwise17Jan.objects.values('sac_number').filter(prabhag_no='122'))
   # print("data_buildings_122_1:",data_buildings_122_1)
   dynamic_detail = list(WasteSegregationDetailsRevised2March22.objects.filter(sac_no__in=data_buildings_122_1))

   sac_numbers = [item['sac_numbers'] for item in dynamic_detail]
   # print(sac_numbers)
   if is_ajax(request=request):
      requestvar = request.get_full_path()
      print("requestvar is ",requestvar)
        
      if "name1" in requestvar:
         today = date.today()
         
         # Yesterday date
         yesterday = today - timedelta(days = 1)
   # if request.is_ajax():
         prabhag = request.GET['name1']
         data= list(MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(prabhag_no=prabhag))
         data_up = list(MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(prabhag_no=prabhag , update_time__contains =yesterday))
         building_list = list(BuildingsWard9April22.objects.filter(prabhag_no=prabhag).values('building_name').order_by('building_name'))
         geojson=serialize('geojson',data)

         if(len(data_up)>1):
            geojson1=serialize('geojson',data_up)
            data = {'geojson':geojson,'geojson1':geojson1,'building_list':building_list}


            return JsonResponse(data, safe=False)
         else:
            data = {'geojson':geojson,'building_list':building_list}
            return JsonResponse(data, safe=False)

      
      elif "name2" in requestvar:
         sel_ward = request.GET['name2']
         prabhag_list = list(MumbaiPrabhagBoundaries3Jan2022V2.objects.filter(ward_id=sel_ward).values('prabhag_no','ward_name','ward_id'))
         
         return JsonResponse(prabhag_list, safe=False)
      else:
         selected_field1 = request.GET['name']
         print("sac number selected is ",selected_field1)
         docinfo1 = list(MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(sac_number=selected_field1).values('sac_number','prop_add','is_bwg','bwg_type','is_compost','compost_type','building_type','building_name','village','road','num_floors','num_flat','population','region','num_shops','wing_name','prabhag_no','ward_name_field','updated_by','update_time','device_ip','address','validity'))
         # docinfo1 = MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(sac_number=selected_field1).values('sac_number','prop_add','is_bwg','bwg_type','is_compost','compost_type','building_type','building_name','village','num_flat','region','num_shops','wing_name','prabhag_no','ward_name_field','updated_by','update_time','device_ip','address','validity')
         jsondata2 =docinfo1[0]
        
         # print(docinfo1[0]);
         return JsonResponse(docinfo1[0])
        
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
         print("prabhag is",prabhag)
         ward_id = list(MumbaiWardBoundary2Jan2022.objects.filter(ward_name_field= ward))
         sel_ward = ward_id[0].ward_id
         prabhag_list = list(MumbaiPrabhagBoundaries3Jan2022V2.objects.filter(ward_id=sel_ward))
         if  request.user.groups.filter(name="prabhagEditor").exists():
            data= list(MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(prabhag_no=prabhag))
            # print("data is",data[0])
         elif  request.user.groups.filter(name="wardEditor").exists():
            data= list(MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(ward_id_2=sel_ward))
         geojson=serialize('geojson',data)
         return render(request,"map/map_new.html",{ 'ward':ward,'prabhag_list':prabhag_list,'prabhag_mumbai':prabhag_mumbai,'ward_list':ward_list,'prabhag':prabhag,'geojson':geojson})
      else:
            # print("no user logged in")
            data= list(MumbaiBuildingsWardPrabhagwise17Jan.objects.all())
            geojson=serialize('geojson',data)
      # obj=Ward61BuildingsOsm2Nov2021.objects.all()
      # kwest  =  KwestBuildingUpdated.objects.all()
      # kwestgeojson =  serialize('geojson',kwest)
            # print(geojson)
#  context = 
      geojson = serialize('geojson',data_buildings_132)
      # print(geojson)
      geojson2 = serialize('geojson',data_buildings_122)
   return render(request,"map/map_new.html",{ 'ward':ward,'prabhag_list':prabhag_list,'ward_list':ward_list,'prabhag':prabhag,'geojson':geojson,'geojson2':geojson2,'prabhag_mumbai':prabhag_mumbai,'dynamic_detail':dynamic_detail})

