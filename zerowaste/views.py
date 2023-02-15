# Create your views here.
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from .forms import (
    GarbageSegForm,
    GrievanceForm,
    Ward61BuildingsOsm2Nov2021Form,
    WasteSegregationDetailsForm,
    NewUserForm,
    EmployeeDetailsForm,
    HumanResourceDataForm,
    MumbaiBuildingsWardPrabhagwise17JanForm,
    WasteSegregationDetailsRevised2march22Form,
    compostForm,
)
from .models import (
    Report,
    Rating,
    WasteSegregationDetails,
    BuildingsWard9April22,
    BuildingUnder30Mtr,
    KWestBeat22Jan,
    WasteSegregationDetailsRevised2March22,
    HumanResourceData,
    P122Buildings8Nov22,
)  # CensusTable #,OsmBuildings29Oct21#BuildingsWardWise4March,
from map.models import (
    Ward61BuildingsOsm2Nov2021,
    MumbaiBuildingsWardPrabhagwise17Jan,
    MumbaiPrabhagBoundaries3Jan2022V2,
    DistinctGeomSacNoMumbai,
)  # ,Ward61OsmBuildings,
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.serializers import serialize

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.contrib.auth.models import Group
from django.db.models import Sum
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, get_connection

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

#######################################################
def HomePage(request):
    return render(request, "HomePage.html")


def restrictedHomePage(request):
    return render(request, "restrictedHomePage.html")


def user_login(request):
    # context = RequestContext(request)
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        print(username, password, user)

        if user is not None:
            # if user.is_active:
            login(request, user)
            messages.info(request, _("Logged in sucessfully."))
            # analytics = initialize_analyticsreporting()
            # response = get_report(analytics)
            # recd_response = print_response(response)
            # context = {
            #     'Visitor_count': recd_response
            # }

            # return render(request, "rating.html", context)
            return render(request, "HomePage.html")
            # else:
            #     # Return a 'disabled account' error message
            #     messages.info(request,_(u"Your account is disabled"))
            #     return HttpResponseRedirect_(u"Your account is disabled.")
        else:
            # Return an 'invalid login' error message.
            print(_("invalid login details for " + username))
            # messages.info(request,"Invalid login details"+ username )
            messages.error(request, _("Invalid username or password."))
            return render(request, "adminlogin.html")
    else:
        return render(request, "adminlogin.html")


def logout_request(request):
    logout(request)
    messages.info(request, _("Logged out successfully!"))
    return render(request, "HomePage.html")


def GarbageSeg(request):
    form = GarbageSegForm()
    if request.method == "POST":
        form = GarbageSegForm(request.POST)
    if form.is_valid():
        regionName = form.cleaned_data["region_name"]
        collDate = form.cleaned_data["coll_date"]
        if regionName == "none":
            messages.warning(request, _("Please select Region"))
        if Report.objects.filter(coll_date=collDate, region_name=regionName).exists():
            messages.warning(request, _("Data already exists for this Zone and Date."))
        else:
            instance = form.save(commit=False)
            instance.save()
            messages.success(
                request,
                _("Your data is saved for {} dated {}").format(regionName, collDate),
            )

        return HttpResponseRedirect(request.path_info)

    else:
        form = GarbageSegForm()

    return render(request, "GarbageSeg.html", {"form": form})
    # return render(request,"GarbageSeg.html")


def show(request):
    datas = Report.objects.all().order_by("-coll_date")
    context = {
        "datas": datas,
        # 'Visitor_count': recd_response
    }

    # return render(request,'show_data.html',{'datas':datas})
    return render(request, "show_data.html", context)


def destroy(request, id):
    data = Report.objects.get(id=id)
    data.delete()
    return redirect("/show/")


def edit(request, id):
    data = Report.objects.get(id=id)
    # docdata  = doctor.objects.get(id=id)
    print(data.id)
    context = {
        "data": data,
        #'Visitor_count': recd_response
    }
    # return render(request,'edit.html', {'data':data})
    return render(request, "edit.html", context)


def update(request, id):
    print(id)
    data = Report.objects.get(id=id)
    # print(data)
    form = GarbageSegForm(request.POST, instance=data)
    print(form)
    if form.is_valid():
        print("success")
        messages.success(request, "Record Updated")
        form.save()
    else:
        print("fail")
        messages.error(request, "Sorry! Record not updated. Try Again")
    context = {
        "data": data,
        #'Visitor_count': recd_response
    }
    print(GarbageSegForm.errors)

    return render(request, "edit.html", context)


def Graphs(request):
    df = pd.read_excel(
        "/home/ubuntu/Documents/ward/MCGM/Ward 61 Waste Collection data.xlsx.xlsx", 0
    )
    df.head(2)

    # Line Chart
    x = df["Do you consume bottle gourd (dudhi/lauki)peel?"].value_counts().index
    fig = px.line(df, x="", y="", color="country")
    fig.show()
    # Bar chart
    # fig = px.bar(df, x = 'What is your Weight? (kgs)', y = 'What is your Height? (cms)', title='Weight to Height ratio')
    # plot_div = plot(fig, output_type='div')

    # Pie Chart
    names = ["White colour", "Orange colour", "No Ration card"]
    fig = px.pie(df, names=names, title="Ration card Holders")
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(title_font_size=42)

    # Bar Chart with count and index
    entities = df["What is your dietary habit?"].value_counts()
    index = entities.index
    fig1 = px.bar(df, x=index, y=entities, title="Dietary Habits")
    fig1.update_layout(title_font_size=42)

    # Grouped Bar Chart with count and index

    fig2 = og.Figure(
        data=[
            og.Bar(
                name="Consume Banana Peel",
                y=df["Do you consume banana peel?"].value_counts(),
                x=df["Do you consume banana peel?"].value_counts().index,
            ),
            og.Bar(
                name="Consume Dudhi (Bottle gourd) Peel",
                y=df["Do you consume bottle gourd (dudhi/lauki)peel?"].value_counts(),
                x=df["Do you consume bottle gourd (dudhi/lauki)peel?"]
                .value_counts()
                .index,
            ),
        ]
    )

    fig2.update_layout(title="Consumption of banana and dudhi peel", title_font_size=42)

    alchemyEngine = create_engine(
        "postgresql://postgres:postgres@localhost/iitb", pool_recycle=3600
    )
    # Connect to PostgreSQL server
    dbConnection = alchemyEngine.connect()
    # Read data from PostgreSQL database table and load into a DataFrame instance
    dataFrame = pd.read_sql('select * from "report"', dbConnection)
    pd.set_option("display.expand_frame_repr", False)
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
    return render(request, "graphs.html")


def Grievance(request):

    # url = staticfiles_storage.path('hostel.csv')
    # url2 = staticfiles_storage.path('hotel_supervisors.csv')
    form = GrievanceForm(request.POST or None)
    if request.method == "POST":
        form = GrievanceForm(request.POST or None)
        myfile = request.FILES["myfile"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        uploaded_file_url = fs.url(filename)

        if form.is_valid():
            # latitude = request.POST.get('latitude')
            # longitude = request.POST.get('longitude')
            cd = form.cleaned_data

            name = form.cleaned_data["name"]
            mobile = form.cleaned_data["mobile"]
            # selectzones = form.cleaned_data['selectzones']

            # selectlanes = form.cleaned_data['selectlanes']
            grievance = form.cleaned_data["grievance"]
            # grievance_no = form.cleaned_data['grievance_no']
            # console.log(grievance_no)
            audio_src = form.cleaned_data["audio_src"]
            img_src = form.cleaned_data["img_src"]
            upload = request.FILES["upload"]

            fss = FileSystemStorage()
            file = fss.save(upload.name, upload)
            file_url = fss.url(file)

            print("Grievance is " + cd["grievance"])
            print("email is " + cd["email"])
            from_email = form.cleaned_data["email"]
            grievance_no = datetime.datetime.now()
            grievance_no = str(grievance_no)
            message_mail = (
                "Senders Name -  "
                + name
                + "\n"
                + "Senders Mobile - "
                + str(mobile)
                + "\n"
                + "Senders Email Id - "
                + from_email
                + "\n"
                + "Grievance Number - "
                + grievance_no
                + "\n"
                + "Grievance Received - "
                + grievance
            )
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

            con = get_connection("django.core.mail.backends.console.EmailBackend")
            con = get_connection("django.core.mail.backends.smtp.EmailBackend")
            to_emails = ["jituviju@gmail.com", "monikapatira@gmail.com"]
            # to_emails.append(supervisor_email_curr)

            print(to_emails)

            if send_mail(
                "Grievance received for mumbai61.nowastes.in",
                message_mail,
                from_email,
                to_emails,
                fail_silently=False,
            ):

                # if(send_mail('Feedback (SWK)', message_mail,from_email,['monikapatira@gmail.com'],fail_silently=False,)):
                print("message sent")
            else:
                console.log(message_mail)
                print("Failure")

            messages.success(
                request,
                _(
                    "Your grievance is saved and email is sent. Your Greivance no. is {}"
                ).format(grievance_no),
            )
            return HttpResponseRedirect(request.path_info)
        else:

            cd = form.cleaned_data
            print(cd)
            print(form.errors)
            messages.warning(request, "Please check your form")
            form_class = GrievanceForm
            #        return render(request,"grievance_form.html",context)

            return render(request, "grievance_form.html", {"form": GrievanceForm})
    else:
        form_class = GrievanceForm

        return render(request, "grievance_form.html", {"form": form_class})


def FAQ(request):
    return render(request, "faq.html")


def FeedbackView(request):
    print(request.method)
    if request.method == "POST":
        name = request.POST.get("name")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        service_swk = request.POST.get("rating1")
        timing_swk = request.POST.get("rating2")
        mobile_swk = request.POST.get("rating3")
        compost_kit_garden = request.POST.get("rating4")
        communicate_swk = request.POST.get("rating5")
        solid_waste_man = request.POST.get("rating6")
        service_workers = request.POST.get("rating7")
        segregation = request.POST.get("rating8")
        recycle_process = request.POST.get("rating9")
        awareness = request.POST.get("rating10")
        role = request.POST.get("rating11")

        sub = Rating(
            name=name,
            mobile=mobile,
            email=email,
            service_swk=service_swk,
            timing_swk=timing_swk,
            mobile_swk=mobile_swk,
            compost_kit_garden=compost_kit_garden,
            communicate_swk=communicate_swk,
            solid_waste_man=solid_waste_man,
            service_workers=service_workers,
            segregation=segregation,
            recycle_process=recycle_process,
            awareness=awareness,
            role=role,
        )
        # if sub.save():
        # print(sub.save)
        sub.save()
        messages.success(request, _(" Your feedback is saved. "))
        return HttpResponseRedirect(request.path_info)
        # else:
        #     messages.warning(request, _(u'Please check your form'))

    return render(request, "feedback_form.html")


def table(request, id):
    requestvar = request.get_full_path()
    print(requestvar)
    data = []
    prabhag = id[-3:]
    if "_up" in id:
        data = list(
            MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(
                prabhag_no=prabhag, update_time__contains=yesterday
            ).values(
                "sac_number",
                "prop_add",
                "building_type",
                "building_name",
                "village",
                "num_flat",
                "region",
                "num_shops",
                "wing_name",
                "prabhag_no",
                "ward_name_field",
                "address",
                "validity",
            )
        )

    else:
        data = list(
            MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(
                prabhag_no=prabhag
            ).values(
                "sac_number",
                "prop_add",
                "building_type",
                "building_name",
                "village",
                "num_flat",
                "region",
                "num_shops",
                "wing_name",
                "prabhag_no",
                "ward_name_field",
                "address",
                "validity",
            )
        )
    # df = pd.DataFrame(data)
    df = json.dumps(data)
    # saving the dataframe
    # df.to_csv('GFG.csv')
    return render(request, "table.html", {"data": df, "id": id, "prabhag": prabhag})


def Buildedit(request, id):
    data = MumbaiBuildingsWardPrabhagwise17Jan.objects.get(sac_number=id)
    print(data)
    # docdata  = doctor.objects.get(id=id)
    # print(data.coll_date)
    context = {
        "data": data,
        #'Visitor_count': recd_response
    }
    # return render(request,'edit.html', {'data':data})
    return render(request, "buildedit.html", context)


def Buildupdate(request, id):

    if is_ajax(request=request):
        print(id)
        id = id.split("-")
        id1 = id[0]
        print("id1")

        MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(sac_number=id1).update(
            validity=True
        )

        return JsonResponse("Success", safe=False)
    # if('-Auth' in id):
    #     print(request.POST)
    #     id = id.split("-")
    #     id1 = id[0]
    #     print("id1")

    #     MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(sac_number=id1).update(validity=True)

    # form = MumbaiBuildingsWardPrabhagwise17JanForm(request.POST, instance=data)
    # print(form)

    if request.method == "POST":
        print("post")
        data = MumbaiBuildingsWardPrabhagwise17Jan.objects.get(sac_number=id)
        if request.user.role == "MO":
            MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(sac_number=id).update(
                validity=True
            )

        print(data)
        form = MumbaiBuildingsWardPrabhagwise17JanForm(request.POST, instance=data)
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
            messages.success(request, "Record Updated")
            form.save()
        else:
            print("fail")
            messages.error(request, "Sorry! Record not updated. Try Again")

    print(Ward61BuildingsOsm2Nov2021Form.errors)

    return redirect("/map/")


def Buildshow(request):
    datas = Ward61OsmBuildings1Nov21.objects.all().order_by("-name")
    # datas1= Tracksheet.objects.all().order_by('-lane_name')
    # wardetail= DutyEntry.objects.all()
    # data= User.objects.all()
    # analytics = initialize_analyticsreporting()
    # response = get_report(analytics)
    # recd_response = print_response(response)
    context = {
        "datas": datas,
        # 'Visitor_count': recd_response
    }

    # return render(request,'show_data.html',{'datas':datas})
    return render(request, "build_show_data.html", context)


# def Ward61OsmBuildings(request):
#     obj = Ward61OsmBuildings.object.all()
#     geojson = serialize('geojson',obj)
#     # console.log(obj)
#     context = {'geojson':geojson}
#     return render(request, "map/map.html", context)


def showwastesegregationdetails(request):
    # datas= WasteSegregationDetails.objects.all().order_by('-coll_date')
    datas = WasteSegregationDetailsRevised2March22.objects.all().order_by("-coll_date")
    context = {
        "datas": datas,
        # 'Visitor_count': recd_response
    }
    return render(request, "show_wsd.html", context)


def WasteSegregationDetailsView(request):
    form = WasteSegregationDetailsForm()
    building = request.POST.get("building_name")
    # form.fields[''].choices = [building.building]
    # print(request.method)
    if request.method == "POST":
        form = WasteSegregationDetailsForm(request.POST)
        # region = form.cleaned_data['region']
        # print(region)
        # regionName = form.cleaned_data['region']
        # print(form['region'].value())
        # print(form['building_cluster'].value())
        if form.is_valid():
            regionName = form.cleaned_data["region"]
            print(regionName)
            collDate = form.cleaned_data["coll_date"]
            if regionName == "none":
                messages.warning(request, _("Please select Region"))
            if WasteSegregationDetails.objects.filter(
                coll_date=collDate, region=regionName
            ).exists():
                messages.warning(
                    request, _("Data already exists for this Zone and Date.")
                )
            else:
                instance = form.save(commit=False)
                instance.save()
                messages.success(
                    request,
                    _("Your data is saved for {} dated {}").format(
                        regionName, collDate
                    ),
                )
                # print(form)
            #   messages.success(request,'Form is valid')
            return HttpResponseRedirect(request.path_info)
        else:
            # print(form['region'].value())
            # print(form['building_cluster'].value())
            form.errors.as_json()
            messages.warning(request, _("Please check your form"))
            messages.warning(request, form.errors.as_json)
    else:
        form = WasteSegregationDetailsForm()
        # print(form)
        form.errors.as_json()
    return render(request, "GarbageSeg.html", {"form": form})
    # return render(request,"GarbageSeg.html")


def load_buildings(request):
    region = request.GET.get("region")
    print("In load buildings" + request.POST.get)
    prabhag_no = request.GET.get("prabhag")
    if prabhag_no == "122":
        building_name = P122Buildings8Nov22.objects.filter(prabhag_no=prabhag_no)
    else:
        building_name = WasteSegregationDetails.objects.filter(region=region)
    print("Building name is " + building_name)
    return render(
        request, "building_dropdown_list_options.html", {"building_name": building_name}
    )


def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


def register_request(request):
    print(request)
    if is_ajax(request=request):

        selected_field1 = request.GET["name"]
        print(selected_field1)
        prabhag_list = list(
            MumbaiPrabhagBoundaries3Jan2022V2.objects.filter(ward_id=selected_field1)
            .values("prabhag_no")
            .order_by("prabhag_no")
        )

        return JsonResponse(prabhag_list, safe=False)

    if request.method == "POST":
        form = NewUserForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return HttpResponseRedirect("../login/")
        messages.error(request, "Unsuccessful registration. Invalid information.")

    form = NewUserForm()
    print(form)
    return render(
        request=request, template_name="register.html", context={"register_form": form}
    )


def group(self, user):
    groups = []
    # user = request.POST.get('username')
    for group in user.groups.all():
        groups.append(group.name)
    return " ".join(groups)


group.short_description = "Groups"

list_display = ("username", "email", "first_name", "last_name", "is_staff", "group")
# The last argument will display a column with the result of the "group" method defined above


def emp_detail(request):
    if request.method == "POST":
        # form = EmployeeDetailsForm('K/W',request.POST or None)
        form = EmployeeDetailsForm(request.POST or None)
        print(request.POST)
        print("Form valid- ", form.is_valid())
        print(form.errors)
        if form.is_valid():
            EmpName = form.cleaned_data["name"]
            EmpMobile = form.cleaned_data["mobile"]
            EmpPost = form.cleaned_data["post"]
            if EmpName == "none":
                messages.warning(request, _("Please Add Employee Name"))
            if EmpMobile == "none":
                EmpMobile = 1111111111
                messages.warning(
                    request,
                    _(
                        "Please Add Employee Number, ELse default no 1111111111 wil be entered."
                    ),
                )
            else:
                instance = form.save(commit=False)
                instance.save()
                print(form)
                messages.success(
                    request,
                    _("Your data is saved for {} as {}").format(EmpName, EmpPost),
                )
                return HttpResponseRedirect(request.path_info)
            # return JsonResponse({"message": 'Got it inside valid'})
        else:
            err = form.errors
            messages.warning(request, form.errors.as_json)
            messages.warning(request, _("Please check your form"))
            return HttpResponseRedirect(request.path_info, {"err": err})
            # return JsonResponse({"message": 'Got it inside invalid'})
    else:
        print(request.method)
        # ward_name = 'K/W'
        # print(ward_name)
        # form = EmployeeDetailsForm(ward_name,request.POST or None)
        form = EmployeeDetailsForm(request.POST or None)
        context = {"form": form}
        return render(request, "EmployeeDetails.html", context)


# from django.core import serializers
def load_prabhag(request):
    ward_n = request.GET.get("name")
    print("ward in load prabhag is " + ward_n)
    # print()
    # prabhag_n = MumbaiPrabhagBoundaries3Jan2022V2.objects.values('prabhag_no').filter(ward_name=ward_n)
    prabhag_n = MumbaiPrabhagBoundaries3Jan2022V2.objects.values("prabhag_no").filter(
        ward_id=ward_n
    )
    print(prabhag_n)
    # prabhag_n=serializers.serialize('json',prabhag_n)
    prabhag_n = list(prabhag_n)
    return JsonResponse({"prabhag_n": prabhag_n})
    # return render(request, 'prabhag_dropdown_list_options.html', {'prabhag_n':prabhag_n})


def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


def hrd_detail(request):
    form = HumanResourceDataForm("S", request.POST or None)
    if is_ajax(request):
        requestvar = request.get_full_path()
        print("Current path " + requestvar)
        if "name" in requestvar:
            selected_field = request.GET["name"]
            print("true")
            print(selected_field)
            docinfo1 = MumbaiPrabhagBoundaries3Jan2022V2.objects.filter(
                ward_name=selected_field
            ).only("prabhag_no")
            # docinfo1 = list(MumbaiPrabhagBoundaries3Jan2022V2.objects.filter(ward_id=selected_field).values);
            # print(docinfo1)
            jsondata2 = docinfo1[0]
            geojson = serialize("geojson", docinfo1, fields=("prabhag_no",))
            print("geojson is:" + geojson)
            data1 = {"geojson": geojson}

            return JsonResponse(data1, safe=False)
            # return geojson.dumps(jsondata2)

    if request.method == "POST":
        # form = HumanResourceDataForm('S',request.POST or None)
        form = HumanResourceDataForm(request.POST or None)
        print(form)
        print(request.POST)
        print("Form valid- ", form.is_valid())
        print(form.errors)
        if form.is_valid():

            EmpName = form.cleaned_data["name_contact_person"]
            EmpMobile = form.cleaned_data["mobile_contact_person"]
            EmpPost = form.cleaned_data["designation"]
            Empprabhag = form.cleaned_data["prabhag"]
            if EmpName == "none":
                messages.warning(request, _("Please Add Employee Name"))
            if EmpMobile == "none":
                EmpMobile = 1111111111
                messages.warning(
                    request,
                    _(
                        "Please Add Employee Number, ELse default no 1111111111 wil be entered."
                    ),
                )
            else:
                instance = form.save(commit=False)
                instance.save()
                print(form)
                messages.success(
                    request,
                    _(
                        "Your data is saved for {} having designation {} in prabhag {}"
                    ).format(EmpName, EmpPost, Empprabhag),
                )
                return HttpResponseRedirect(request.path_info)
            # return JsonResponse({"message": 'Got it inside valid'})
        else:

            messages.warning(request, form.errors.as_json)
            messages.warning(request, _("Please check your form"))

            return HttpResponseRedirect(request.path_info)
            # return JsonResponse({"message": 'Got it inside invalid'})
    else:
        print(request.method)
        # user_info.objects.values_list('name', flat=True).distinct()
        # ward_name = 'S'
        # print(ward_name)
        # form = HumanResourceDataForm(ward_name,request.POST or None)
        ward_list = list(MumbaiPrabhagBoundaries3Jan2022V2.objects.values("ward_name"))
        form = HumanResourceDataForm(request.POST or None)
        context = {"form": form}
        return render(request, "HRDDetails.html", context)


def resources(request):
    return render(request, "Resources.html")


def base(request):
    # ward_region = WasteSegregationDetails.objects.values('re').annotate(Sum('wet_waste_before_segregation') , Sum('dry_waste_before_segregation'), Sum('hazardous_waste')  )

    map_ward = WasteSegregationDetails.objects.values("ward").annotate(
        Sum("wet_waste_before_segregation"),
        Sum("dry_waste_before_segregation"),
        Sum("hazardous_waste"),
    )
    line_region = WasteSegregationDetails.objects.values("coll_date").annotate(
        Sum("wet_waste_before_segregation"),
        Sum("dry_waste_before_segregation"),
        Sum("hazardous_waste"),
    )
    map_region = WasteSegregationDetails.objects.values("region").annotate(
        Sum("wet_waste_before_segregation"),
        Sum("dry_waste_before_segregation"),
        Sum("hazardous_waste"),
    )
    line_date_region = WasteSegregationDetails.objects.values(
        "coll_date", "region"
    ).annotate(
        Sum("wet_waste_before_segregation"),
        Sum("dry_waste_before_segregation"),
        Sum("hazardous_waste"),
    )

    # data = WasteSegregationDetails.objects.values('region','wet_waste_before_segregation','dry_waste_before_segregation','hazardous_waste')
    # data=WasteSegregationDetails.objects.values('region','wet_waste_before_segregation','dry_waste_before_segregation','hazardous_waste').annotate(Count('region')).order_by()
    new_data = json.dumps(list(map_ward), cls=DjangoJSONEncoder)
    region_data = json.dumps(list(map_region), cls=DjangoJSONEncoder)
    date_region = json.dumps(list(line_date_region), cls=DjangoJSONEncoder)
    date_new_data = json.dumps(list(line_region), cls=DjangoJSONEncoder)

    return render(
        request,
        "home.html",
        {
            "ward": new_data,
            "date_data": date_new_data,
            "region": region_data,
            "date_region_line": date_region,
        },
    )


def w61wcd(request):
    df = pd.read_excel(
        "/home/ubuntu/Documents/Diet-Diversity/Nutri-infotainment survey (Part 1) (Responses).xlsx",
        0,
    )
    df.head(2)
    # Bar chart
    # fig = px.bar(df, x = 'What is your Weight? (kgs)', y = 'What is your Height? (cms)', title='Weight to Height ratio')
    # plot_div = plot(fig, output_type='div')

    # Pie Chart
    names = ["White colour", "Orange colour", "No Ration card"]
    fig = px.pie(df, names=names, title="Ration card Holders")
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(title_font_size=42)

    # Bar Chart with count and index
    entities = df["What is your dietary habit?"].value_counts()
    index = entities.index
    fig1 = px.bar(df, x=index, y=entities, title="Dietary Habits")
    fig1.update_layout(title_font_size=42)

    # Grouped Bar Chart with count and index

    fig2 = og.Figure(
        data=[
            og.Bar(
                name="Consume Banana Peel",
                y=df["Do you consume banana peel?"].value_counts(),
                x=df["Do you consume banana peel?"].value_counts().index,
            ),
            og.Bar(
                name="Consume Dudhi (Bottle gourd) Peel",
                y=df["Do you consume bottle gourd (dudhi/lauki)peel?"].value_counts(),
                x=df["Do you consume bottle gourd (dudhi/lauki)peel?"]
                .value_counts()
                .index,
            ),
        ]
    )

    fig2.update_layout(title="Consumption of banana and dudhi peel", title_font_size=42)

    alchemyEngine = create_engine(
        "postgresql://postgres:postgres@localhost/iitb", pool_recycle=3600
    )
    # Connect to PostgreSQL server
    dbConnection = alchemyEngine.connect()
    # Read data from PostgreSQL database table and load into a DataFrame instance
    dataFrame = pd.read_sql('select * from "report"', dbConnection)
    pd.set_option("display.expand_frame_repr", False)
    dataFrame.plot(y="kitchen waste in kg", x="coll_date")
    plt.show()

    # data = [og.Scatter(x="coll_date")]

    # Print the DataFrame
    print(dataFrame)
    # Close the database connection

    dbConnection.close()

    plot_div = plot(fig, output_type="div")
    plot_div1 = plot(fig1, output_type="div")
    plot_div2 = plot(fig2, output_type="div")
    # plot_div3 = plot(fig3,output_type='div')
    return render(
        request,
        "w61wcd.html",
        context={"plot_div": plot_div, "plot_div1": plot_div1, "plot_div2": plot_div2},
    )


def dashboard2(request):
    return render(request, "dashboard2/index.html")


def Piecharts(request):
    return render(request, "piecharts.html")


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

        road = request.GET["road"]
        print(road)
        data = list(KWestBeat22Jan.objects.filter(fid=road))

        # data_up = list(MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(prabhag_no=prabhag , update_time__contains =yesterday))
        building_list = list(BuildingUnder30Mtr.objects.filter(fid_2=road))
        geojson = serialize("geojson", data)

        geojson1 = serialize("geojson", building_list)
        data = {"geojson": geojson, "geojson1": geojson1}

        return JsonResponse(data, safe=False)
    if request.method == "GET":
        prabhag_list = list(
            KWestBeat22Jan.objects.values("fid", "name")
            .exclude(name__isnull=True)
            .distinct()
        )
        print(prabhag_list)
        return render(request, "road_buf.html", {"prabhag_list": prabhag_list})


def WasteSegregationDetailsRevisedView(request):
    form = WasteSegregationDetailsRevised2march22Form()
    # building = request.POST.get('building_name')
    # form.fields[''].choices = [building.building]
    print(request.method)
    userName = request.user
    print("username is ", userName)
    if is_ajax(request=request):
        requestvar = request.get_full_path()
        print(requestvar)

        if "prabhag" in requestvar:
            selected_field1 = request.GET["prabhag"]
            print("Prabhag select " + selected_field1)
            # prabhag_list = list(BuildingsWardWise4March.objects.filter(prabhag_no=selected_field1).values('road_name').order_by('road_name').distinct())
            if selected_field1 == "122":
                print("In s ward")
                prabhag_list = list(
                    P122Buildings8Nov22.objects.filter(prabhag_no=selected_field1)
                    .values("building_n")
                    .order_by("building_n")
                    .distinct()
                )
                sac_list = list(
                    P122Buildings8Nov22.objects.filter(prabhag_no=selected_field1)
                    .values("sac_number")
                    .order_by("sac_number")
                )
            else:
                prabhag_list = list(
                    BuildingsWard9April22.objects.filter(prabhag_no=selected_field1)
                    .values("road_name")
                    .order_by("road_name")
                    .distinct()
                )
                sac_list = list(
                    MumbaiBuildingsWardPrabhagwise17Jan.objects.filter(
                        prabhag_no=selected_field1
                    )
                    .values("sac_number")
                    .order_by("sac_number")
                )
            data = {"prabhag_list": prabhag_list, "sac_list": sac_list}
            return JsonResponse(data, safe=False)
        elif "ward" in requestvar:
            selected_field1 = request.GET["ward"]
            print(selected_field1)
            prabhag_list = list(
                MumbaiPrabhagBoundaries3Jan2022V2.objects.filter(
                    ward_id=selected_field1
                )
                .values("prabhag_no")
                .order_by("prabhag_no")
            )

            return JsonResponse(prabhag_list, safe=False)
        elif "road" in requestvar:
            selected_field1 = request.GET["road"]
            print(selected_field1)
            # prabhag_list = list(BuildingsWardWise4March.objects.filter(road_name=selected_field1).values('building_name').order_by('building_name'))
            prabhag_list = list(
                BuildingsWard9April22.objects.filter(road_name=selected_field1)
                .values("building_name")
                .order_by("building_name")
            )
            return JsonResponse(prabhag_list, safe=False)

        elif "building_name" in requestvar:
            selected_field1 = request.GET["building_name"]
            print(selected_field1)
            prabhag_list = list(
                BuildingsWard9April22.objects.filter(road_name=selected_field1)
                .values("building_name")
                .order_by("building_name")
            )
            return JsonResponse(prabhag_list, safe=False)
    if request.method == "POST":
        form = WasteSegregationDetailsRevised2march22Form(request.POST)
        # region = form.cleaned_data['region']
        # print(region)
        # regionName = form.cleaned_data['region']
        # print(form['region'].value())
        # print(form['building_cluster'].value())

        if form.is_valid():
            sacNo = form.cleaned_data["sac_no"]
            # print(regionName)
            collDate = form.cleaned_data["coll_date"]
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
            messages.success(
                request, _("Your data is saved for date {}").format(collDate)
            )
            print(form)
            return HttpResponseRedirect(request.path_info)

            # messages.warning(request,form.errors.as_json)
    else:
        form = WasteSegregationDetailsRevised2march22Form()
        print(form)
        form.errors.as_json()
    return render(request, "GarbageSegRevised.html", {"form": form})


def compost_form(request):
<<<<<<< HEAD
    form = compostForm()
    if request.method == "POST":
        form = compostForm(request.POST)
        if form.is_valid():
            collDate = form.cleaned_data["coll_date"]
            # a.username = request.user
            print(collDate)
            form.save()
            # task_list.username = request.user.username
            # print(instance)
            # instance.save()
            messages.success(
                request, _("Your data is saved for date {}").format(collDate)
            )
=======
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
>>>>>>> e827dfbdf438d3586ff26efc83b7a8a6c422db6d
            print(form)
            return HttpResponseRedirect(request.path_info)
        else:
            # print(form['region'].value())
            # print(form['building_cluster'].value())
            form.errors.as_json()
            messages.warning(request, _("Please check your form"))
    else:
        form = compostForm()
        print(form)
        form.errors.as_json()
    return render(request, "CompostForm.html", {"form": form})
