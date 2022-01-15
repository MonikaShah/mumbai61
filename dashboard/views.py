from django.shortcuts import render
from django.views.generic import View
from .models import Ward61BuildingsOsm2Nov2021, WasteSegregationDetails 
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum

# Create your views here.

class Dash(View):
    template_name = "dashboard/dashboard.html"

    def get(self, request, *args, **kwargs):
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

        map_ward = WasteSegregationDetails.objects.values('ward','coll_date').annotate(Sum('wet_waste_before_segregation') , Sum('dry_waste_before_segregation'), Sum('hazardous_waste')  )
        line_region = WasteSegregationDetails.objects.values('coll_date').annotate(Sum('wet_waste_before_segregation') , Sum('dry_waste_before_segregation'), Sum('hazardous_waste')  )
        map_region = WasteSegregationDetails.objects.values('region').annotate(Sum('wet_waste_before_segregation') , Sum('dry_waste_before_segregation'), Sum('hazardous_waste')  )
        line_date_region = WasteSegregationDetails.objects.values('coll_date','region').annotate(Sum('wet_waste_before_segregation') , Sum('dry_waste_before_segregation'), Sum('hazardous_waste')  )

        # data = WasteSegregationDetails.objects.values('region','wet_waste_before_segregation','dry_waste_before_segregation','hazardous_waste')
        # data=WasteSegregationDetails.objects.values('region','wet_waste_before_segregation','dry_waste_before_segregation','hazardous_waste').annotate(Count('region')).order_by()

        # kwest  =  AllPropDataKwest.objects.all()
        # geojson=serialize('geojson',obj)
        # kwestgeojson =  serialize('geojson',kwest)
        max_date = WasteSegregationDetails.objects.latest('coll_date').coll_date
        month_date = 1
        
        last6Months = (months[max_date.month -6:max_date.month])


        new_data = json.dumps(list(map_ward), cls=DjangoJSONEncoder)
        region_data = json.dumps(list(map_region), cls=DjangoJSONEncoder)
        date_region = json.dumps(list(line_date_region), cls=DjangoJSONEncoder)
        date_new_data = json.dumps(list(line_region), cls=DjangoJSONEncoder)

        # print(map_region)
        context = {'ward':new_data,'date_data':date_new_data,"region": region_data,"date_region_line":date_region}
        return render(request, self.template_name,context)

