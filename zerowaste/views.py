# Create your views here.
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from .forms import GarbageSegForm,GrievanceForm,aggregatorRequestorLoginForm,Ward61BuildingsOsm2Nov2021Form,WasteSegregationDetailsForm,NewUserForm,EmployeeDetailsForm,HumanResourceDataForm,MumbaiBuildingsWardPrabhagwise17JanForm,WasteSegregationDetailsRevised2march22Form,compostForm,dataForm,DocumentForm,reportForm,AggregatorForm,WasteSegregationDetailsRevised2march22FormNew,BuildingDailyForm
from .models import Report,Rating,WasteSegregationDetails,BuildingsWard9April22,BuildingUnder30Mtr,KWestBeat22Jan,WasteSegregationDetailsRevised2March22,HumanResourceData,P122Buildings8Nov22, data_form,links,document_up,AggregatorData,AggregatorRequestorLogin,BuildingDaily #CensusTable #,OsmBuildings29Oct21#BuildingsWardWise4March
from map.models import Ward61BuildingsOsm2Nov2021,MumbaiBuildingsWardPrabhagwise17Jan,MumbaiPrabhagBoundaries3Jan2022V2,DistinctGeomSacNoMumbai#,Ward61OsmBuildings,
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
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail,get_connection
from django.conf import settings
# from django.contrib import messages
import datetime
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from operator import is_not
from functools import partial

import plotly.express as px
from plotly.offline import plot

import plotly.graph_objects as og
import numpy

from django.shortcuts import render
from wagtail.documents.models import Document
import os
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.core.files.storage import default_storage
from django.core.files import File
import simplejson as json
from django.db.models import Count
from datetime import datetime
from django.db.models.functions import Cast
from django.db.models import F
# import geojson
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

def document_list(request):
    documents = Document.objects.all()
    return render(request, 'document_list.html', {'documents': documents})

def static_files_view(request):
    static_folder = 'zerowaste/static/'
    folder_path = 'resources'
    files = os.listdir(static_folder)
    folder_full_path = os.path.join(static_folder, folder_path)
    files = os.listdir(folder_full_path)
    
    context = {
        'files': files,
        'folder_path': folder_path
    }
    return render(request, 'template.html', context)

def HomePage(request):
    return render(request,"HomePage.html")

def restrictedHomePage(request):
    return render(request,"restrictedHomePage.html")

def user_login(request):
    # context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print(username,password,user)
        
        if user is not None:
            # if user.is_active: 
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
            # else:
            #     # Return a 'disabled account' error message
            #     messages.info(request,_(u"Your account is disabled"))
            #     return HttpResponseRedirect_(u"Your account is disabled.")
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

def reset_pass(request):
    # logout(request)
    # messages.info(request, _(u"Logged out successfully!"))
    return render(request,"password_reset_form.html")

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
    df = pd.read_excel('/home/ubuntu/Documents/ward/MCGM/Ward 61 Waste Collection data.xlsx.xlsx',0)
    df.head(2)

    #Line Chart 
    x = df['Do you consume bottle gourd (dudhi/lauki)peel?'].value_counts().index
    fig = px.line(df, x="", y="", color='country')
    fig.show()
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
    form = GrievanceForm(request.POST,request.FILES)
    media_url=settings.MEDIA_URL
    if request.method == 'POST' and 'myfile' not in request.FILES and 'upload' not in request.FILES :
        form = GrievanceForm(request.POST or None)
        
        if form.is_valid():
            cd = form.cleaned_data
            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobile']
            grievance = form.cleaned_data['grievance']
            
            audio_src = form.cleaned_data['audio_src']
            img_src = form.cleaned_data['img_src']
           
            print("Grievance is "+cd['grievance'])
            print("email is "+ cd['email'])
            from_email_actual = form.cleaned_data['email']
            
            from_email = settings.EMAIL_HOST_USER
            grievance_no = datetime.datetime.now()
            grievance_no = str(grievance_no)
            message_mail = 'Senders Name -  '+ name + "\n" + 'Senders Mobile - '+ str(mobile) + "\n" + 'Senders Email Id - ' +from_email_actual + "\n" +'Grievance Number - ' + grievance_no +"\n"+ 'Grievance Received - '+ grievance
            
            print(from_email)
            print(request.POST)
            form.save()
            
            con = get_connection('django.core.mail.backends.smtp.EmailBackend')
            
            
            to_emails = ['monika.shah2003@gmail.com']
            # to_emails.append(supervisor_email_curr)

            print(to_emails)

            if(send_mail('Grievance received for mumbai.nowastes.in', message_mail,from_email,to_emails,fail_silently=False,)):
            
            # if(send_mail('Feedback (SWK)', message_mail,from_email,['monikapatira@gmail.com'],fail_silently=False,)):
                print("message sent")
    if request.method == 'POST' and 'myfile' in request.FILES and 'upload' in request.FILES :
        form = GrievanceForm(request.POST,request.FILES)
        myfile = request.FILES['myfile']
        
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
 
        if form.is_valid():
            cd = form.cleaned_data
            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobile']
            grievance = form.cleaned_data['grievance']
            
            audio_src = form.cleaned_data['audio_src']
            img_src = form.cleaned_data['img_src']
           
            upload = request.FILES['upload']
            fss = FileSystemStorage()
            file = fss.save(upload.name, upload)
            file_url = fss.url(file)

           
            print("Grievance is "+cd['grievance'])
            print("email is "+ cd['email'])
            # from_email = form.cleaned_data['email']
            from_email = settings.EMAIL_HOST_USER
            grievance_no = datetime.datetime.now()
            grievance_no = str(grievance_no)
            message_mail = 'Senders Name -  '+ name + "\n" + 'Senders Mobile - '+ str(mobile) + "\n" + 'Senders Email Id - ' +from_email + "\n" +'Grievance Number - ' + grievance_no +"\n"+ 'Grievance Received - '+ grievance 
            image_path =  filename       
            # print(from_email)
            # print(request.POST)
            # message_mail.mixed_subtype = 'related'
            # message_mail.attach_alternative(body_html, "text/html")
            # with default_storage.open(image_path, 'rb') as image_file:
            #     message_mail.attach(image_path, image_file.read(), 'image/png')  # Adjust content type as needed
            
            message_mail.attach(myfile.name, myfile.read(), myfile.content_type)          
            form.save()
            
            con = get_connection('django.core.mail.backends.smtp.EmailBackend')
            
            
            to_emails = ['monika.shah2003@gmail.com']
            # to_emails.append(supervisor_email_curr)

            print(to_emails)

            if(send_mail('Grievance received for mumbai.nowastes.in', message_mail,from_email,to_emails,fail_silently=False,)):
            
            # if(send_mail('Feedback (SWK)', message_mail,from_email,['monikapatira@gmail.com'],fail_silently=False,)):
                print("message sent")
            else :
                print(message_mail)
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
def table(request,id):
    requestvar = request.get_full_path()
    print(requestvar)
    data = []
    prabhag = id[-3:]
    data_ward_list = list(MumbaiPrabhagBoundaries3Jan2022V2.objects.filter(prabhag_no=prabhag).values('ward_name'))
    data_ward = data_ward_list[0]['ward_name'] if data_ward_list else None
    print("ward name is",data_ward)
    if '_up' in id:
        data = list(MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(prabhag_no=prabhag , update_time__contains =yesterday).values('sac_number','prop_add','building_type','building_name','village','num_flat','region','num_shops','wing_name','prabhag_no','ward_name_field','address','validity'))

    else:
        data= list(MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(prabhag_no=prabhag,ward_name_field=data_ward).values('sac_number','address','village','building_type','building_name','region','road','num_flat','num_shops','population','prabhag_no','ward_name_field','validity'))
    # df = pd.DataFrame(data) 
    df =json.dumps(data) 
# saving the dataframe 
    # df.to_csv('GFG.csv') 
    return render(request,'table.html',{'data':df,'id':id,'prabhag':prabhag}) 

def Buildedit(request, id):  
    data = MumbaiBuildingsWardPrabhagwise17Jan.objects.get(sac_number=id)
    print(data)
    # docdata  = doctor.objects.get(id=id)  
    # print(data.coll_date)
    context = {
        'data':data,
        #'Visitor_count': recd_response
    }
    # return render(request,'edit.html', {'data':data}) 
    return render(request,'buildedit.html',context) 

def Buildupdate(request, id):
    
    if is_ajax(request=request):
        print(id)
        id = id.split("-")
        id1 = id[0]
        print("id1")

        MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(sac_number=id1).update(validity=True)

        return JsonResponse("Success", safe=False)
    # if('-Auth' in id):
    #     print(request.POST)
    #     id = id.split("-")
    #     id1 = id[0]
    #     print("id1")

    #     MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(sac_number=id1).update(validity=True)
        
        
        # form = MumbaiBuildingsWardPrabhagwise17JanForm(request.POST, instance=data)
        # print(form)  
    
    if request.method == 'POST':
        print("post")
        data = MumbaiBuildingsWardPrabhagwise17Jan.objects.get(sac_number=id) 
        if request.user.role == "MO":
            MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(sac_number=id).update(validity=True)

        print("data is ",data) 
        form = MumbaiBuildingsWardPrabhagwise17JanForm(request.POST, instance=data)  
        # print("instance " ,form)
        
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
            # print("Form is ",form) 
            messages.success(request,"Record Updated")          
            if form.save():
                print ("Data saved in db")
                for key, value in request.POST.items():
                    print('Key: %s' % (key) ) 
                    print('Value- %s' % (value) )
                # return redirect('/buildupdate/'+id)
            else:
                print("error in saving to DB")
        else:
            print("fail")
            messages.error(request,"Sorry! Record not updated. Try Again")
    
    print(MumbaiBuildingsWardPrabhagwise17JanForm.errors)
    
    return redirect("/map/") 
    

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
    # datas= WasteSegregationDetails.objects.all().order_by('-coll_date')
    datas= WasteSegregationDetailsRevised2March22.objects.all().order_by('-coll_date')
    context = {
        'datas':datas,
        # 'Visitor_count': recd_response
    }
    return render(request,'show_wsd.html',context)

def showdailystatus_interns(request):
    # datas= WasteSegregationDetails.objects.all().order_by('-coll_date')
    datas= MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(updated_by__in=('siddiqui', 'Sakina Syed','AshishG','riteshhhyadav248@gmail.com','Monika_N_132')).annotate(updated_by_count=Count('updated_by'))
    # daily_count = MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(ward_name_field='N').values('updated_by',updated_time_date=datetime.strptime('update_time', '%Y-%m-%d')).annotate(updated_by_count=Count('updated_by')).order_by('updated_by','update_time')
    context = {
        'datas':datas,
        # 'daily_count':daily_count,
        # 'Visitor_count': recd_response
    }
    return render(request,'show_dailystat.html',context)

def WasteSegregationDetailsView(request):
        form = WasteSegregationDetailsForm()
        building = request.POST.get('building_name')
        # form.fields[''].choices = [building.building]
        # print(request.method)
        if request.method == 'POST':
            form = WasteSegregationDetailsForm(request.POST)
            ## region = form.cleaned_data['region']
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
    print("In load buildings"+request.POST.get)
    prabhag_no=request.GET.get('prabhag')
    if(prabhag_no=='122'):
        building_name = P122Buildings8Nov22.objects.filter(prabhag_no=prabhag_no)
    else:
        building_name = WasteSegregationDetails.objects.filter(region=region)
    print("Building name is "+building_name)
    return render(request, 'building_dropdown_list_options.html', {'building_name': building_name})

def is_ajax(request):
   return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
def register_request(request):
    print(request)
    if is_ajax(request=request):

      selected_field1 = request.GET['name']
      print(selected_field1)
      prabhag_list = list(MumbaiPrabhagBoundaries3Jan2022V2.objects.filter(ward_id=selected_field1).values('prabhag_no').order_by('prabhag_no'))

   
      return JsonResponse(prabhag_list, safe=False)
    
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return HttpResponseRedirect('../login/')
        messages.error(request, "Unsuccessful registration. Invalid information.")
        
    form = NewUserForm()
    print(form)
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
        # form = EmployeeDetailsForm('K/W',request.POST or None)
        form = EmployeeDetailsForm(request.POST or None)
        print(request.POST)
        print ("Form valid- ",form.is_valid())
        print (form.errors)     
        if form.is_valid():            
            EmpName = form.cleaned_data['name']
            EmpMobile =form.cleaned_data['mobile']
            EmpPost =form.cleaned_data['post']
            if EmpName =="none":
                messages.warning(request, _(u'Please Add Employee Name'))
            if EmpMobile =="none":
                EmpMobile = 1111111111
                messages.warning(request, _(u'Please Add Employee Number, ELse default no 1111111111 wil be entered.'))
            else:
                instance = form.save(commit=False)
                instance.save()
                print(form)
                messages.success(request, _(u'Your data is saved for {} as {}').format(EmpName,EmpPost))
                return HttpResponseRedirect(request.path_info)
            # return JsonResponse({"message": 'Got it inside valid'})
        else:
            err=form.errors
            messages.warning(request,form.errors.as_json)
            messages.warning(request, _(u'Please check your form'))
            return HttpResponseRedirect(request.path_info,{'err':err})
            # return JsonResponse({"message": 'Got it inside invalid'})
    else:
        print(request.method)
        # ward_name = 'K/W'
        # print(ward_name)
        # form = EmployeeDetailsForm(ward_name,request.POST or None)
        form = EmployeeDetailsForm(request.POST or None)
        context= {
        'form': form}
        return render(request, 'EmployeeDetails.html',context)
# from django.core import serializers
def load_prabhag(request):
    ward_n = request.GET.get('name')
    print("ward in load prabhag is "+ ward_n)
    #print()
    # prabhag_n = MumbaiPrabhagBoundaries3Jan2022V2.objects.values('prabhag_no').filter(ward_name=ward_n)
    prabhag_n = MumbaiPrabhagBoundaries3Jan2022V2.objects.values('prabhag_no').filter(ward_id=ward_n)
    print(prabhag_n)
    #prabhag_n=serializers.serialize('json',prabhag_n)
    prabhag_n = list(prabhag_n)
    return JsonResponse({"prabhag_n":prabhag_n})
    #return render(request, 'prabhag_dropdown_list_options.html', {'prabhag_n':prabhag_n})
def is_ajax(request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'   
        
def hrd_detail(request):
    form = HumanResourceDataForm('S',request.POST or None)
    if is_ajax(request):     
        requestvar = request.get_full_path()
        print("Current path "+requestvar)
        if "name" in requestvar:
            selected_field = request.GET['name']
            print("true")
            print(selected_field)
            docinfo1 = MumbaiPrabhagBoundaries3Jan2022V2.objects.filter(ward_name=selected_field).only('prabhag_no'); 
            # docinfo1 = list(MumbaiPrabhagBoundaries3Jan2022V2.objects.filter(ward_id=selected_field).values); 
            # print(docinfo1)
            jsondata2 =docinfo1[0]
            geojson=serialize('geojson',docinfo1,fields=('prabhag_no',))
            print("geojson is:"+geojson)
            data1 = {'geojson':geojson}

            return JsonResponse(data1, safe=False)
            # return geojson.dumps(jsondata2)     



    if request.method == "POST":
        # form = HumanResourceDataForm('S',request.POST or None)
        form = HumanResourceDataForm(request.POST or None)
        print(form)
        print(request.POST)
        print ("Form valid- ",form.is_valid())
        print (form.errors)     
        if form.is_valid():      
            
            EmpName = form.cleaned_data['name_contact_person']
            EmpMobile =form.cleaned_data['mobile_contact_person']
            EmpPost =form.cleaned_data['designation']
            Empprabhag = form.cleaned_data['prabhag']
            if EmpName =="none":
                messages.warning(request, _(u'Please Add Employee Name'))
            if EmpMobile =="none":
                EmpMobile = 1111111111
                messages.warning(request, _(u'Please Add Employee Number, ELse default no 1111111111 wil be entered.'))
            else:
                instance = form.save(commit=False)
                instance.save()
                print(form)
                messages.success(request, _(u'Your data is saved for {} having designation {} in prabhag {}').format(EmpName,EmpPost,Empprabhag))
                return HttpResponseRedirect(request.path_info)
            # return JsonResponse({"message": 'Got it inside valid'})
        else:
            
            messages.warning(request,form.errors.as_json)
            messages.warning(request, _(u'Please check your form'))
            
            return HttpResponseRedirect(request.path_info)
            # return JsonResponse({"message": 'Got it inside invalid'})
    else:
        print(request.method)
        # user_info.objects.values_list('name', flat=True).distinct()
        # ward_name = 'S'
        # print(ward_name)
        # form = HumanResourceDataForm(ward_name,request.POST or None)
        ward_list=list(MumbaiPrabhagBoundaries3Jan2022V2.objects.values('ward_name'))
        form = HumanResourceDataForm(request.POST or None)
        context= {
        'form': form}
        return render(request, 'HRDDetails.html',context)


def resources(request):
    document = document_up.objects.all()
    # print(documents)
    # image = image_up_sch.objects.all()
    # video = video_sch.objects.all()
    return render(request,'Resources.html',{'document': document})

def resources_orig(request):
    document = document_up.objects.all()
    # print(documents)
    # image = image_up_sch.objects.all()
    # video = video_sch.objects.all()
    return render(request,'Resources_orig26oct23.html')

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

def w61wcd(request):
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

    plot_div = plot(fig, output_type='div')
    plot_div1 = plot(fig1,output_type='div')
    plot_div2 = plot(fig2,output_type='div')
    # plot_div3 = plot(fig3,output_type='div')
    return render(request,'w61wcd.html', context={'plot_div': plot_div, 'plot_div1':plot_div1,'plot_div2':plot_div2 })

def dashboard2(request):
    return render(request,'test-2/index.html')


def dashboard2_1(request):
    return render(request,'test3/index.html')

def dashboard2_2(request):
    return render(request,'test4/index.html')

def Piecharts(request):
    return render(request,'piecharts.html')
    
# def tree_census_charts(request):
#     census_table_csv_data = CensusTable.objects.all()

#     df = pd.DataFrame(census_table_csv_data.values())
    
#     print(df.columns)
#     fig = px.histogram(df, x = 'name_of_the_city')
#     plt.xlabel('Number of Trees')
#     plt.ylabel('Cities')
#     fig.write_image('zerowaste/static/charts/tree-city.png')
#     plt.close()
    
    
#     # fig = px.pie(df,values='name_of_the_city',names=df['tree_type']=='Indegenious')
#     fig = px.histogram(df[df['tree_type']=='Indegenious'], x = 'name_of_the_city')
#     plt.xlabel('Number of Indegenious Trees')
#     plt.ylabel('Cities')
#     fig.write_image('zerowaste/static/charts/indegenious-city.png')
#     plt.close()
    
#     fig = px.bar(df, x='tree_common_name', y= 'total_area_in_sq_kms_under_all_trees')
#     plt.xlabel('Common Name of the tree')
#     plt.ylabel('Total are in sq kms under all tree')
#     plt.xticks(rotation=40)
#     fig.write_image('zerowaste/static/charts/tree-area.png')
#     plt.close()

#     no_of_heritage_trees = len(df[df['current_tree_age'] >= 50])
#     no_of_newly_planted_trees = len(df[df['current_tree_age'] <= 25])
#     total_area_under_indegenious_trees = sum(df['total_area_in_sq_kms_under_native_indegeniuos_trees'].tolist())
#     total_area_under_all_trees = sum(df['total_area_in_sq_kms_under_all_trees'].tolist())
#     trees_under_govt_land = sum(df[df['tree_ownership_plantation_initiated_by'] == 'Government']['total_area_in_sq_kms_under_all_trees'].tolist())
#     trees_under_private_land = sum(df[df['tree_ownership_plantation_initiated_by'] == 'Private']['total_area_in_sq_kms_under_all_trees'].tolist())
#     trees_under_other_land = sum(df[df['tree_ownership_plantation_initiated_by'] == 'Others']['total_area_in_sq_kms_under_all_trees'].tolist())

#     print(no_of_heritage_trees)
#     print(no_of_newly_planted_trees)
#     print(total_area_under_indegenious_trees)
#     print(total_area_under_all_trees)
#     print(trees_under_govt_land)
#     print(trees_under_private_land)
#     print(trees_under_other_land)

#     context = {
#         'heritage_trees' : no_of_heritage_trees,
#         'newly_planted_trees' : no_of_newly_planted_trees,
#         'area_under_indegenious_trees' : total_area_under_indegenious_trees,
#         'area_under_all_trees' : total_area_under_all_trees,
#         'govt_land_trees' : trees_under_govt_land,
#         'private_land_trees' : trees_under_private_land,
#         'other_land_trees' : trees_under_other_land
#     }


#     return render(request,'tree_census_charts.html')
def road_bufferView(request):
    if is_ajax(request=request):
        requestvar = request.get_full_path()
        print(requestvar)
            
      
        road = request.GET['road']
        print(road)
        data= list(KWestBeat22Jan.objects.filter(fid=road))
        
        # data_up = list(MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(prabhag_no=prabhag , update_time__contains =yesterday))
        building_list = list(BuildingUnder30Mtr.objects.filter(fid_2=road))
        geojson=serialize('geojson',data)

        geojson1=serialize('geojson',building_list)
        data = {'geojson':geojson,'geojson1':geojson1}


        return JsonResponse(data, safe=False)
    if request.method == 'GET':
        prabhag_list = list(KWestBeat22Jan.objects.values('fid','name').exclude(name__isnull=True).distinct())
        print(prabhag_list)
        return render(request,'road_buf.html',{'prabhag_list':prabhag_list})

def WasteSegregationDetailsRevisedView_new(request):
        # print("sac no is",id)
        # sac_no=id
        form = WasteSegregationDetailsRevised2march22FormNew()
        # building = request.POST.get('building_name')
        # form.fields[''].choices = [building.building]
        print(request.method)
        userName = request.user
        print("username is ",userName)
        if is_ajax(request=request):
            requestvar = request.get_full_path()
            print(requestvar)
               
            if "prabhag" in requestvar:
                selected_field1 = request.GET['prabhag']
                print("Prabhag select "+selected_field1)
                # prabhag_list = list(BuildingsWardWise4March.objects.filter(prabhag_no=selected_field1).values('road_name').order_by('road_name').distinct())
                if(selected_field1=='122'):
                    print("In s ward")
                    prabhag_list = list(P122Buildings8Nov22.objects.filter(prabhag_no=selected_field1).values('building_n').order_by('building_n').distinct())
                    sac_list = list(P122Buildings8Nov22.objects.filter(prabhag_no=selected_field1).values('sac_number').order_by('sac_number'))
                else:
                    prabhag_list = list(BuildingsWard9April22.objects.filter(prabhag_no=selected_field1).values('road_name').order_by('road_name').distinct())
                    sac_list = list(MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(prabhag_no=selected_field1).values('sac_number').order_by('sac_number'))
                data = {'prabhag_list':prabhag_list,'sac_list':sac_list}
                return JsonResponse(data, safe=False)
            elif "ward" in requestvar:
                selected_field1 = request.GET['ward']
                print(selected_field1)
                prabhag_list = list(MumbaiPrabhagBoundaries3Jan2022V2.objects.filter(ward_id=selected_field1).values('prabhag_no').order_by('prabhag_no'))
      
                return JsonResponse(prabhag_list, safe=False)
            elif "road" in requestvar:
                selected_field1 = request.GET['road']
                print(selected_field1)
                # prabhag_list = list(BuildingsWardWise4March.objects.filter(road_name=selected_field1).values('building_name').order_by('building_name'))
                prabhag_list = list(BuildingsWard9April22.objects.filter(road_name=selected_field1).values('building_name').order_by('building_name'))
                return JsonResponse(prabhag_list, safe=False)

            elif "building_name" in requestvar:
                selected_field1 =request.GET['building_name']
                print(selected_field1)
                prabhag_list = list(BuildingsWard9April22.objects.filter(road_name=selected_field1).values('building_name').order_by('building_name'))
                return JsonResponse(prabhag_list, safe=False)
        if request.method == 'POST':
            form = WasteSegregationDetailsRevised2march22FormNew(request.POST)
            ## region = form.cleaned_data['region']
            # print(region)
            # regionName = form.cleaned_data['region']
            # print(form['region'].value())
            # print(form['building_cluster'].value())
            
            if form.is_valid():
                sacNo = form.cleaned_data['sac_no']
                # print(regionName)
                collDate = form.cleaned_data['coll_date']
                # userName = form.cleaned_data['user_nm']
                # if regionName =="none":
                #     messages.warning(request, _(u'Please select Region'))
                # if  WasteSegregationDetails.objects.filter(coll_date=collDate, region=regionName).exists():
                #     messages.warning(request, _(u'Data already exists for this Zone and Date.'))
                # else:  
                    # instance = form.save(commit=False)
                    # instance.save()
                    # messages.success(request, _(u'Your data is saved for {} dated {}').format(regionName,collDate))
                    # print(form)
                #   messages.success(request,'Form is valid')
                # form.save()
                a = form.save(commit=False)
                a.username = request.user
                print(a.username.username)
                a.save()
                # task_list.username = request.user.username
                # print(instance)
                # instance.save()
                messages.success(request, _(u'Your data is saved for date {}').format(collDate))
                print(form)
                return HttpResponseRedirect(request.path_info)
            
            
                # messages.warning(request,form.errors.as_json)
        else:
                
                form = WasteSegregationDetailsRevised2march22FormNew()
                print(form)
                form.errors.as_json()
                # print("sac is",sac_no)
        return render(request, 'GarbageSegRevised.html', {'form': form})

def WasteSegregationDetailsRevisedView(request,id):
        print("sac no is",id)
        sac_no=id

        form = WasteSegregationDetailsRevised2march22Form()
        form1 = BuildingDailyForm()
        print(form1)
        my_list_1 = ''
        # building = request.POST.get('building_name')
        # form.fields[''].choices = [building.building]
        print(request.method)
        userName = request.user
        print("username is ",userName)
        if is_ajax(request=request):
            requestvar = request.get_full_path()
            print(requestvar)
               
            if "prabhag" in requestvar:
                selected_field1 = request.GET['prabhag']
                print("Prabhag select "+selected_field1)
                # prabhag_list = list(BuildingsWardWise4March.objects.filter(prabhag_no=selected_field1).values('road_name').order_by('road_name').distinct())
                if(selected_field1=='122'):
                    print("In s ward")
                    prabhag_list = list(P122Buildings8Nov22.objects.filter(prabhag_no=selected_field1).values('building_n').order_by('building_n').distinct())
                    sac_list = list(P122Buildings8Nov22.objects.filter(prabhag_no=selected_field1).values('sac_number').order_by('sac_number'))
                else:
                    print("In other ward")
                    prabhag_list = list(BuildingsWard9April22.objects.filter(prabhag_no=selected_field1).values('road_name').order_by('road_name').distinct())
                    sac_list = list(MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(prabhag_no=selected_field1).values('sac_number').order_by('sac_number'))
                data = {'prabhag_list':prabhag_list,'sac_list':sac_list}
                return JsonResponse(data, safe=False)
            elif "ward" in requestvar:
                selected_field1 = request.GET['ward']
                print(selected_field1)
                prabhag_list = list(MumbaiPrabhagBoundaries3Jan2022V2.objects.filter(ward_id=selected_field1).values('prabhag_no').order_by('prabhag_no'))
      
                return JsonResponse(prabhag_list, safe=False)
            elif "road" in requestvar:
                selected_field1 = request.GET['road']
                print(selected_field1)
                # prabhag_list = list(BuildingsWardWise4March.objects.filter(road_name=selected_field1).values('building_name').order_by('building_name'))
                prabhag_list = list(BuildingsWard9April22.objects.filter(road_name=selected_field1).values('building_name').order_by('building_name'))
                return JsonResponse(prabhag_list, safe=False)

            elif "building_name" in requestvar:
                selected_field1 =request.GET['building_name']
                print(selected_field1)
                prabhag_list = list(BuildingsWard9April22.objects.filter(road_name=selected_field1).values('building_name').order_by('building_name'))
                return JsonResponse(prabhag_list, safe=False)
        if request.method == 'POST':
            form = WasteSegregationDetailsRevised2march22Form(request.POST)
            form1 = BuildingDailyForm()
            
            if form.is_valid():
                print("forms are valid")
                
                specific_values = {
                    'wet_waste':form.cleaned_data['wet_waste'],
                    'dry_waste':form.cleaned_data['dry_waste'],
                    'primary_id':form.cleaned_data['sac_no'],
                    'parent_id':"6",
                    'date':form.cleaned_data['coll_date']
                
                }
                # sacNo = form.cleaned_data['sac_no']
                # print(regionName)
                collDate = form.cleaned_data['coll_date']
               
                a = form.save(commit=False)
                a.username = request.user
                print(a.username.username)
                a.save()
            # if form1.is_valid():
                
                b= form1.save(commit=False)
                # b=BuildingDaily(**specific_values)
                b.parent_id=specific_values['parent_id']
                b.dry_waste=specific_values['dry_waste']
                b.wet_waste=specific_values['wet_waste']
                b.primary_id=specific_values['primary_id']
                b.total_waste=b.dry_waste + b.wet_waste
                
                b.population=100
                b.weight=b.total_waste/b.population
                b.date=collDate
                b.save()
                print(form1)
                print("form1 is also valid",form1.errors)
                
                messages.success(request, _(u'Your data is saved for date {}').format(collDate))
                print(form)
                return HttpResponseRedirect(request.path_info)
            else:
                print("invalid forms")
                form1.errors.as_json()
                print(form1.errors)
                messages.warning(request,form1.errors.as_json)
            
                # messages.warning(request,form.errors.as_json)
        else:
                             
                my_list= MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(sac_number=id).values('building_name','ward_name_field','prabhag_no','road').order_by('building_name')
                my_list_1 = my_list[0]
                bldg_name = my_list_1.get('building_name')
                ward_name = my_list_1.get('ward_name_field')
                prabhag_name = my_list_1.get('prabhag_no')
                road_name = my_list_1.get('road')
                print("my list is",my_list_1.get('building_name'))
                # print("building name in list is ".item['desired_value'])
                initial_data = {'sac_no': sac_no,'building_name':bldg_name,'ward_name':ward_name,'prabhag_name':prabhag_name,'road_name':road_name}
                form = WasteSegregationDetailsRevised2march22Form(initial=initial_data)
                
                # print(form)
                form.errors.as_json()
                print("sac is",sac_no)
        return render(request, 'GarbageSegRevised.html', {'form': form,'form1':form1,'sac_no':sac_no,'my_list_1':my_list_1})

def compost_form(request):
        form = compostForm()
        if request.method == 'POST':
            form = compostForm(request.POST)
            if form.is_valid():
                collDate = form.cleaned_data['coll_date']
                a = form.save(commit=False)
                a.username = request.user
                print(a.username.username)
                a.save()
                # task_list.username = request.user.username
                # print(instance)
                # instance.save()
                messages.success(request, _(u'Your data is saved for date {}').format(collDate))
                print(form)
                return HttpResponseRedirect(request.path_info)
                
            else:
               
                form.errors.as_json()
                messages.warning(request, _(u'Please check your form'))
        else:
            form = compostForm()
            print(form)
            form.errors.as_json()
        return render(request, 'CompostForm.html', {'form': form})

def student_registration(req):
    for key, value in req.POST.items():
                print('Key: %s' % (key) ) 
                print('Value %s' % (value) )
    user = req.user
    # mail = req.email
    username = user.username
    emailid = user.email
    print(username,emailid)
    # request_dict = vars(req)
    # print(request_dict)
    # print(req)
    # age = .['age']
    if req.method == 'POST':
            emailF = emailid
            studentName = req.POST['sname']
            age = req.POST['age']
            websiteUsername = username
            collegeName = req.POST['cname']
            sponsered = req.POST['sponsered']
            sponsBy = req.POST['sponsBy']
            ownDevice = req.POST['ownDevice']
            date = req.POST['datE']  
            # grad_year = req.POST['grad_year']
            #grad_stream = req.POST['grad_stream']
            # branch_name= req.POST['branch_name']
            # village_name = req.POST['village_name']
            # taluka_name = req.POST['taluka_name']
            # river_name = req.POST['river_name']
            # dist_river_village = req.POST['dist_river_village']
            # field_work_map = req.POST['rating1']
            # digitisation = req.POST['rating2']
            # trip_data_capture = req.POST['rating3']
            # coding = req.POST['rating4']

            # form = dataForm(req.POST)
            totalData = data_form(emailF=emailF,studentName=studentName,age=age,collegeName=collegeName,websiteUsername=websiteUsername,sponsered=sponsered,sponsBy=sponsBy,ownDevice=ownDevice,date=date)

            # totalData = data_form(emailF=emailF,studentName=studentName,age=age,collegeName=collegeName,websiteUsername=websiteUsername,sponsered=sponsered,sponsBy=sponsBy,ownDevice=ownDevice,date=date,grad_year=grad_year,grad_stream=grad_stream,branch_name=branch_name,village_name=village_name,taluka_name=taluka_name,river_name=river_name,dist_river_village=dist_river_village,field_work_map=field_work_map,digitisation=digitisation,trip_data_capture=trip_data_capture,coding=coding)
            # print(studentName)
            if  data_form.objects.filter(emailF=emailF).exists():
                    messages.warning(req, _(u'Student with this "Email" has already been registered. '))        
                    return render(req, 'HomePage.html')
            elif  data_form.objects.filter(websiteUsername=websiteUsername).exists():
                messages.warning(req,"Username already exists.")
                # return HttpResponseRedirect(req.path_info)
                return render(req, 'HomePage.html')
            else:
                totalData.save()
                messages.info(req,"Student succesfully registered.")
                return render(req, 'HomePage.html')
                
    return render(req, 'student_registration_form.html')


def static_files_view(request):
    # static_folder = 'dashboard/static/'
    # folder_path = 'doc'
    # files = os.listdir(static_folder)
    # folder_full_path = os.path.join(static_folder, folder_path)
    # files = os.listdir(folder_full_path)
    # documents=Document.objects.all()
    # images = Image.objects.all()
    link=links.objects.all()
    context = {
        # 'files': files,
        # 'folder_path': folder_path,
        # 'documents':documents,
        # 'images': images,
        'links': link,
        
    }
    return render(request, 'videos.html', context)

def list_articles(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request,"Article is uploaded.")
            # return redirect('/resources/')
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    # documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(request,'list_articles.html',{'form': form})

def plr_map(request):
    return render(request, 'map/plr_map.html')

def plr_report(request):
  
        form = reportForm()
        if request.method == 'POST':
            form = reportForm(request.POST)
            if form.is_valid():
                collDate = form.cleaned_data['date']
                a = form.save(commit=False)
                a.username = request.user
                print(a.username.username)
                a.save()
                # task_list.username = request.user.username
                # print(instance)
                # instance.save()
                messages.success(request, _(u'Your data is saved for date {}').format(collDate))
                print(form)
                return HttpResponseRedirect(request.path_info)
                
            else:
               
                form.errors.as_json()
                messages.warning(request, _(u'Please check your form'))
        else:
            form = reportForm()
            print(form)
            form.errors.as_json()
        return render(request, 'report_nuisance.html', {'form': form})
    
def aggregatorForm(request):
    form = AggregatorForm()
    userName = request.user
    print(userName)
    if request.method == 'POST':
            form = AggregatorForm(request.POST)
    if form.is_valid():
        address = form.cleaned_data['address']
        shop_name= form.cleaned_data['shop_name']
        owner_name = form.cleaned_data['owner_name']
        mobile= form.cleaned_data['mobile']
        pincode=form.cleaned_data['pincode']
        # username=userName
        if address =="none":
            messages.warning(request, _(u'Please add Address'))
        if shop_name =="none":
            messages.warning(request, _(u'Please fill shop/stall name'))
        if owner_name =="none":
            messages.warning(request, _(u'Please fill your name'))
        if pincode =="none":
            messages.warning(request, _(u'Please fill pincode'))
        if mobile =="none":
            messages.warning(request, _(u'Please fill contact number'))

        # if  AggregatorData.objects.filter(username=username).exists():
            # messages.warning(request, _(u'You are already registered.'))
        else:  
            instance = form.save(commit=False)
            instance.username =userName
            instance.save()
            messages.success(request, _(u'Congrats ! {} is added as aggregator.').format(userName))
        
        return HttpResponseRedirect(request.path_info)

    else:
        form = AggregatorForm()
        print("In aggregator form")

    context ={}
    context['form']= AggregatorForm()
    return render(request, 'aggregator.html',context)

def aggregatorRequestorLogin(request):
    form = aggregatorRequestorLoginForm()
    formDict = {'form': form}
    
    if request.method == 'POST':
        form = aggregatorRequestorLoginForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        phone= form.cleaned_data['phone']
        email = form.cleaned_data['email']
        password= form.cleaned_data['password']
        role=form.cleaned_data['role']
        
        if password =="none":
            messages.warning(request, _(u'Please add password'))
        if email =="none":
            messages.warning(request, _(u'Please fill your email address'))
        if name =="none":
            messages.warning(request, _(u'Please fill your name'))
        if phone =="none":
            messages.warning(request, _(u'Please fill contact number'))
        if role =="none":
            messages.warning(request, _(u'Please select your role.'))
        
        else:  
            instance = form.save(commit=False)
            instance.email =email
            instance.save()
            messages.success(request, _(u'Congrats ! {} are registered.').format(email))
        
        # return HttpResponseRedirect(request.path_info)

    else:
        form = aggregatorRequestorLoginForm()
        print(form.errors)
        print("In aggregator requestor login form")
        print(form.errors)
        print(form.non_field_errors())

    # context ={}
    # context['form']= aggregatorRequestorLoginForm()
    return render(request, 'aggr_Requ_login.html',context=formDict)

    