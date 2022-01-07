# Create your views here.
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from .forms import GarbageSegForm,GrievanceForm,Ward61BuildingsOsm2Nov2021Form,WasteSegregationDetailsForm,NewUserForm,EmployeeDetailsForm,KwestBuildingUpdatedForm
from .models import Report,Rating,WasteSegregationDetails #,OsmBuildings29Oct21
from map.models import Ward61BuildingsOsm2Nov2021,KwestBuildingUpdated#,Ward61OsmBuildings,
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.serializers import serialize
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User,auth
from django.contrib.auth.models import Group
from django.db.models import Sum
import json
from django.core.serializers.json import DjangoJSONEncoder

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail,get_connection
# from django.contrib import messages
import datetime
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

import plotly.express as px
from plotly.offline import plot

import plotly.graph_objects as og
import numpy
###From Akshita's Dashboard##############
# import pandas as pd
# import json
# import plotly.express as px  # (version 4.7.0 or higher)
# import plotly.graph_objects as go
# # import plotly.express as px
# # import dash, dcc, html, Input, Output

# import dash_bootstrap_components as dbc
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output, State

#######################################################
def HomePage(request):
    return render(request,"HomePage.html")

def user_login(request):
    # context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active: 
                login(request, user)
                messages.info(request,_(u"Logged in sucessfully."))
                # analytics = initialize_analyticsreporting()
                # response = get_report(analytics)
                # recd_response = print_response(response)
                # context = {
                #     'Visitor_count': recd_response
                # }

                # return render(request, "rating.html", context)
                return render(request,"HomePage.html")
            else:
                # Return a 'disabled account' error message
                messages.info(request,_(u"Your account is disabled"))
                return HttpResponseRedirect_(u"Your account is disabled.")
        else:
            # Return an 'invalid login' error message.
            print (_(u"invalid login details for " + username))
            # messages.info(request,"Invalid login details"+ username )
            messages.error(request, _(u"Invalid username or password."))
            return render(request,'adminlogin.html')
    else:
        return render(request,'adminlogin.html')

def logout_request(request):
    logout(request)
    messages.info(request, _(u"Logged out successfully!"))
    return render(request,"HomePage.html")


def GarbageSeg(request):
        form = GarbageSegForm()
        if request.method == 'POST':
                form = GarbageSegForm(request.POST)
        if form.is_valid():
            regionName = form.cleaned_data['region_name']
            collDate = form.cleaned_data['coll_date']
            if regionName =="none":
                messages.warning(request, _(u'Please select Region'))
            if  Report.objects.filter(coll_date=collDate, region_name=regionName).exists():
                messages.warning(request, _(u'Data already exists for this Zone and Date.'))
            else:  
                instance = form.save(commit=False)
                instance.save()
                messages.success(request, _(u'Your data is saved for {} dated {}').format(regionName,collDate))
            
            return HttpResponseRedirect(request.path_info)

        else:
                form = GarbageSegForm()

        return render(request, 'GarbageSeg.html', {'form': form})
        # return render(request,"GarbageSeg.html")
def show(request):
    datas= Report.objects.all().order_by('-coll_date')
    context = {
        'datas':datas,
        # 'Visitor_count': recd_response
    }
    
    # return render(request,'show_data.html',{'datas':datas})
    return render(request,'show_data.html',context)

def destroy(request, id):  
    data = Report.objects.get(id=id)  
    data.delete()  
    return redirect("/show/") 

def edit(request, id):  
    data = Report.objects.get(id=id)
    # docdata  = doctor.objects.get(id=id)  
    print(data.id)
    context = {
        'data':data,
        #'Visitor_count': recd_response
    }
    # return render(request,'edit.html', {'data':data}) 
    return render(request,'edit.html',context) 

def update(request, id):
    print(id)
    data = Report.objects.get(id=id) 
    # print(data) 
    form = GarbageSegForm(request.POST, instance=data)  
    print(form)
    if form.is_valid(): 
        print("success") 
        messages.success(request,"Record Updated")          
        form.save()          
    else:
        print("fail")
        messages.error(request,"Sorry! Record not updated. Try Again")
    context = {
        'data':data,
        #'Visitor_count': recd_response
        } 
    print(GarbageSegForm.errors)
    
    return render(request,'edit.html',context) 
    

def Graphs(request):
    df = pd.read_excel('/home/ubuntu/Documents/Diet-Diversity/Nutri-infotainment survey (Part 1) (Responses).xlsx',0)
    df.head(2)
    # Bar chart 
    # fig = px.bar(df, x = 'What is your Weight? (kgs)', y = 'What is your Height? (cms)', title='Weight to Height ratio')
    # plot_div = plot(fig, output_type='div')
    
    # Pie Chart
    names = ['White colour', 'Orange colour', 'No Ration card']
    fig = px.pie(df, names=names, title ='Ration card Holders')
    fig.update_traces(
        textposition = 'inside',
        textinfo = 'percent+label'
    )
    fig.update_layout(
        title_font_size = 42
    )

    # Bar Chart with count and index
    entities = df['What is your dietary habit?'].value_counts()
    index = entities.index
    fig1 = px.bar(df, x=index, y=entities, title= 'Dietary Habits')
    fig1.update_layout(
        title_font_size = 42
    )

     # Grouped Bar Chart with count and index

    fig2 = og.Figure(data=[og.Bar(
    name = 'Consume Banana Peel',
    y = df['Do you consume banana peel?'].value_counts(),
    x = df['Do you consume banana peel?'].value_counts().index
   ),
    og.Bar(
    name = 'Consume Dudhi (Bottle gourd) Peel',
    y = df['Do you consume bottle gourd (dudhi/lauki)peel?'].value_counts(),
    x = df['Do you consume bottle gourd (dudhi/lauki)peel?'].value_counts().index
   )   
])
     
    
    fig2.update_layout(
    title ='Consumption of banana and dudhi peel',
    title_font_size = 42
    )

    

    alchemyEngine   = create_engine('postgresql://postgres:postgres@localhost/iitb', pool_recycle=3600);
# Connect to PostgreSQL server
    dbConnection    = alchemyEngine.connect()
# Read data from PostgreSQL database table and load into a DataFrame instance
    dataFrame       = pd.read_sql("select * from \"report\"", dbConnection);
    pd.set_option('display.expand_frame_repr', False)
    dataFrame.plot(y="kitchen waste in kg", x="coll_date")
    plt.show()

    # data = [og.Scatter(x="coll_date")]
    
# Print the DataFrame
    print(dataFrame)
# Close the database connection

    dbConnection.close()

    # plot_div = plot(fig, output_type='div')
    # plot_div1 = plot(fig1,output_type='div')
    # plot_div2 = plot(fig2,output_type='div')
    # plot_div3 = plot(fig3,output_type='div')
    # return render(request,'graphs.html', context={'plot_div': plot_div, 'plot_div1':plot_div1,'plot_div2':plot_div2 })
    return render(request,'graphs.html')

def Grievance(request):

    # url = staticfiles_storage.path('hostel.csv')
    # url2 = staticfiles_storage.path('hotel_supervisors.csv')
    form = GrievanceForm(request.POST or None)
    if request.method == 'POST':
        form = GrievanceForm(request.POST or None)
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        
        uploaded_file_url = fs.url(filename)
 
        if form.is_valid():
            # latitude = request.POST.get('latitude')
            # longitude = request.POST.get('longitude')
            cd = form.cleaned_data

            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobile']
            # selectzones = form.cleaned_data['selectzones']
            
            # selectlanes = form.cleaned_data['selectlanes']
            grievance = form.cleaned_data['grievance']
            # grievance_no = form.cleaned_data['grievance_no']
            # console.log(grievance_no)
            audio_src = form.cleaned_data['audio_src']
            img_src = form.cleaned_data['img_src']
            upload = request.FILES['upload']

            fss = FileSystemStorage()
            file = fss.save(upload.name, upload)
            file_url = fss.url(file)

           
            print("Grievance is "+cd['grievance'])
            print("email is "+ cd['email'])
            from_email = form.cleaned_data['email']
            grievance_no = datetime.datetime.now()
            grievance_no = str(grievance_no)
            message_mail = 'Senders Name -  '+ name + "\n" + 'Senders Mobile - '+ str(mobile) + "\n" + 'Senders Email Id - ' +from_email + "\n" +'Grievance Number - ' + grievance_no +"\n"+ 'Grievance Received - '+ grievance
            # message_mail = 'Senders Name -  '+ name + "\n" + 'Senders Mobile - '+ str(mobile) + "\n" + 'Senders Email Id - ' +from_email + "\n"  + 'Grievance for Zone -' +selectzones + "\n" + 'Grievance of lane - ' +selectlanes + "\n"+ 'Grievance Number - '+grievance_no +"\n"+ 'Grievance Received - '+ grievance
            # message_mail = 'Senders Name -  '+ name + "\n" + 'Senders Mobile - '+ str(mobile) + "\n" + 'Senders Email Id - ' +from_email + "\n" 
            # + 'Is collecting food waste once a day enough? - '+ fw_once + "\n"
            # + 'Would you like to collect food waste twice a day enough? - '+ str(fw_twice) + "\n"
            # + 'Do you have container for food waste? - '+ str(fw_container) + "\n"
            # + 'Do you have container for dry waste? - '+ str(dw_container) + "\n"
            # + 'Do you have container for menstrual waste? - '+ str(mw_container) + "\n"
            # + 'Do you have container for e-waste waste? - '+ str(ew_container) + "\n"
            # + 'Feedback Received - '+ feedback

            # print(latitude)
            # print(request.POST.get('lat'))
            print(from_email)
            print(request.POST)
            form.save()
            

            con = get_connection('django.core.mail.backends.console.EmailBackend')
            con = get_connection('django.core.mail.backends.smtp.EmailBackend')
            to_emails = ['jituviju@gmail.com', 'monikapatira@gmail.com']
            # to_emails.append(supervisor_email_curr)

            print(to_emails)

            if(send_mail('Grievance received for mumbai61.nowastes.in', message_mail,from_email,to_emails,fail_silently=False,)):
            
            # if(send_mail('Feedback (SWK)', message_mail,from_email,['monikapatira@gmail.com'],fail_silently=False,)):
                print("message sent")
            else :
                console.log(message_mail)
                print("Failure")

            messages.success(request, _(u'Your grievance is saved and email is sent. Your Greivance no. is {}' ).format(grievance_no))
            return HttpResponseRedirect(request.path_info)
        else:
           
            cd = form.cleaned_data
            print(cd)
            print(form.errors)
            messages.warning(request, 'Please check your form')
            form_class = GrievanceForm
    #        return render(request,"grievance_form.html",context)

            return render(request, 'grievance_form.html',{'form': GrievanceForm})
    else: 
        form_class = GrievanceForm
       

        return render(request, "grievance_form.html", {'form': form_class})


def FAQ(request):
    return render(request, "faq.html")

def FeedbackView(request):
        print(request.method)
        if request.method == 'POST':
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email')
            service_swk = request.POST.get('rating1')
            timing_swk = request.POST.get('rating2')
            mobile_swk = request.POST.get('rating3')
            compost_kit_garden = request.POST.get('rating4')
            communicate_swk = request.POST.get('rating5')
            solid_waste_man = request.POST.get('rating6')
            service_workers = request.POST.get('rating7')
            segregation = request.POST.get('rating8')
            recycle_process = request.POST.get('rating9')
            awareness = request.POST.get('rating10')
            role =  request.POST.get('rating11')    
                   
            sub=Rating(name=name,mobile=mobile,email=email,service_swk=service_swk,timing_swk=timing_swk,mobile_swk=mobile_swk,compost_kit_garden=compost_kit_garden,communicate_swk=communicate_swk,solid_waste_man=solid_waste_man,service_workers=service_workers,segregation=segregation,recycle_process=recycle_process,awareness=awareness,role=role)
            # if sub.save():
                # print(sub.save)
            sub.save()
            messages.success(request, _(u' Your feedback is saved. '))
            return HttpResponseRedirect(request.path_info)
            # else:
            #     messages.warning(request, _(u'Please check your form'))
        
        

        return render(request, "feedback_form.html")
def Buildedit(request, id):  
    data = KwestBuildingUpdated.objects.get(sac_no=id)
    # docdata  = doctor.objects.get(id=id)  
    # print(data.coll_date)
    context = {
        'data':data,
        #'Visitor_count': recd_response
    }
    # return render(request,'edit.html', {'data':data}) 
    return render(request,'buildedit.html',context) 

def Buildupdate(request, id):
    # print(id)
    data = KwestBuildingUpdated.objects.get(sac_no=id) 
    # print(data) 
    form = KwestBuildingUpdatedForm(request.POST, instance=data)  
    print(form)
    # if form.is_valid(): 
    #     print("success") 
    #     form.save()  
    #     return render("/buildshow/")  
    # else:
    #     print("fail")
    
    # context = {
    #     'data':data,
    #     #'Visitor_count': recd_response
    # }
    if form.is_valid(): 
        print("success") 
        messages.success(request,"Record Updated")          
        form.save()          
    else:
        print("fail")
        messages.error(request,"Sorry! Record not updated. Try Again")
    context = {
        'data':data,
        #'Visitor_count': recd_response
        } 
    print(Ward61BuildingsOsm2Nov2021Form.errors)
    
    return render(request,'buildedit.html',context) 
    

def Buildshow(request):
    datas= Ward61OsmBuildings1Nov21.objects.all().order_by('-name')
    # datas1= Tracksheet.objects.all().order_by('-lane_name')
    # wardetail= DutyEntry.objects.all()
    # data= User.objects.all()
    # analytics = initialize_analyticsreporting()
    # response = get_report(analytics)
    # recd_response = print_response(response)
    context = {
        'datas':datas,
        # 'Visitor_count': recd_response
    }
    
    # return render(request,'show_data.html',{'datas':datas})
    return render(request,'build_show_data.html',context)

# def Ward61OsmBuildings(request):
#     obj = Ward61OsmBuildings.object.all()
#     geojson = serialize('geojson',obj)
#     # console.log(obj)
#     context = {'geojson':geojson}
#     return render(request, "map/map.html", context)

def showwastesegregationdetails(request):
    datas= WasteSegregationDetails.objects.all().order_by('-coll_date')
    context = {
        'datas':datas,
        # 'Visitor_count': recd_response
    }
    return render(request,'show_wsd.html',context)

def WasteSegregationDetailsView(request):
        form = WasteSegregationDetailsForm()
        building = request.POST.get('building_name')
        # form.fields[''].choices = [building.building]
        # print(request.method)
        if request.method == 'POST':
            form = WasteSegregationDetailsForm(request.POST)
            # region = form.cleaned_data['region']
            # print(region)
            # regionName = form.cleaned_data['region']
            # print(form['region'].value())
            # print(form['building_cluster'].value())
            if form.is_valid():
                regionName = form.cleaned_data['region']
                print(regionName)
                collDate = form.cleaned_data['coll_date']
                if regionName =="none":
                    messages.warning(request, _(u'Please select Region'))
                if  WasteSegregationDetails.objects.filter(coll_date=collDate, region=regionName).exists():
                    messages.warning(request, _(u'Data already exists for this Zone and Date.'))
                else:  
                    instance = form.save(commit=False)
                    instance.save()
                    messages.success(request, _(u'Your data is saved for {} dated {}').format(regionName,collDate))
                    # print(form)
                #   messages.success(request,'Form is valid')
                return HttpResponseRedirect(request.path_info)
            else:
                # print(form['region'].value())
                # print(form['building_cluster'].value())
                form.errors.as_json()
                messages.warning(request, _(u'Please check your form'))
                messages.warning(request,form.errors.as_json)
        else:
                form = WasteSegregationDetailsForm()
                # print(form)
                form.errors.as_json()
        return render(request, 'GarbageSeg.html', {'form': form})
        # return render(request,"GarbageSeg.html")
def load_buildings(request):
    region = request.GET.get('region')
    building_name = WasteSegregationDetails.objects.filter(region=region)
    return render(request, 'building_dropdown_list_options.html', {'building_name': building_name})

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return HttpResponseRedirect('../login/')
		messages.error(request, "Unsuccessful registration. Invalid information.")
        
        
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})

def group(self, user):
    groups = []
    # user = request.POST.get('username')
    for group in user.groups.all():
        groups.append(group.name)
    return ' '.join(groups)
group.short_description = 'Groups'

list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'group')
# The last argument will display a column with the result of the "group" method defined above


def emp_detail(request):
    if request.method == "POST":
        form = EmployeeDetailsForm(request.POST or None)
               
        if form.is_valid():
            EmpName = form.cleaned_data['emp_name']
            EmpMobile =form.cleaned_data['emp_mobile']
            EmpPost =form.cleaned_data['emp_category']
            if EmpName =="none":
                messages.warning(request, _(u'Please Add Employee Name'))
            if EmpMobile =="none":
                EmpMobile = 11111111
                messages.warning(request, _(u'Please Add Employee Number, ELse default no 1111111111 wil be entered.'))
            else:
                instance = form.save(commit=False)
                instance.save()
                print(form)
                messages.success(request, _(u'Your data is saved for {} as {}').format(EmpName,EmpPost))
                return HttpResponseRedirect(request.path_info)
        else:
            messages.warning(request, _(u'Please check your form'))
    else:
        form = EmployeeDetailsForm(request.POST or None)
        context= {
        'form': form}
        return render(request, 'EmployeeDetails.html',context)

def resources(request):
    return render(request,'Resources.html')

def base(request):
    # ward_region = WasteSegregationDetails.objects.values('re').annotate(Sum('wet_waste_before_segregation') , Sum('dry_waste_before_segregation'), Sum('hazardous_waste')  )

    map_ward = WasteSegregationDetails.objects.values('ward').annotate(Sum('wet_waste_before_segregation') , Sum('dry_waste_before_segregation'), Sum('hazardous_waste')  )
    line_region = WasteSegregationDetails.objects.values('coll_date').annotate(Sum('wet_waste_before_segregation') , Sum('dry_waste_before_segregation'), Sum('hazardous_waste')  )
    map_region = WasteSegregationDetails.objects.values('region').annotate(Sum('wet_waste_before_segregation') , Sum('dry_waste_before_segregation'), Sum('hazardous_waste')  )
    line_date_region = WasteSegregationDetails.objects.values('coll_date','region').annotate(Sum('wet_waste_before_segregation') , Sum('dry_waste_before_segregation'), Sum('hazardous_waste')  )
    
    # data = WasteSegregationDetails.objects.values('region','wet_waste_before_segregation','dry_waste_before_segregation','hazardous_waste')
    # data=WasteSegregationDetails.objects.values('region','wet_waste_before_segregation','dry_waste_before_segregation','hazardous_waste').annotate(Count('region')).order_by()
    new_data = json.dumps(list(map_ward), cls=DjangoJSONEncoder)
    region_data = json.dumps(list(map_region), cls=DjangoJSONEncoder)
    date_region = json.dumps(list(line_date_region), cls=DjangoJSONEncoder)
    date_new_data = json.dumps(list(line_region), cls=DjangoJSONEncoder)

    return render(request,"home.html",{'ward':new_data,'date_data':date_new_data,"region": region_data,"date_region_line":date_region})