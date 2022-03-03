from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

from .models import Report,Grievance,WasteSegregationDetails,EmployeeDetails,User,MumbaiBuildingsWardPrabhagwise17Jan,WasteSegregationDetailsRevised2March22#,OsmBuildings29Oct21
from map.models import Ward61BuildingsOsm2Nov2021
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, ButtonHolder
import datetime
# from phonenumber_field.formfields import PhoneNumberField
from django.contrib.gis import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from datetime import timedelta
# import pandas as pd
# import numpy as np
import xlrd
import csv

councillorWard = [
    ('Ward 61','Ward 61'),
    ('Ward 59','Ward 59'),
    ('Ward 60','Ward 60'),
    ('Ward 62','Ward 62'),
    ('Ward 63','Ward 63'),
    ('Ward 64','Ward 64'),
    ('Ward 65','Ward 65'),
    ('Ward 66','Ward 66'),
    ('Ward 67','Ward 67'),
    ('Ward 68','Ward 68'),
    ('Ward 69','Ward 69'),
    ('Ward 70','Ward 70'),
    ('Ward 71','Ward 71'),
]
Regions = [
    ('Anandnagar','Anandnagar'),
    ('Behram baug Kadam Nagar','Behram baug Kadam Nagar'),
    ('Behram Baugh Parasi Colony','Behram Baugh Parasi Colony'),
    ('BMC colony','BMC colony'),
    ('BMC Plot','BMC Plot'),
    ('Fakeer Waadi','Fakeer Waadi'),
    ('Ganesh Nagar','Ganesh Nagar'),
    ('Gujarat Bhavan','Gujarat Bhavan'),
    ('Gyansagar','Gyansagar'),
    ('Heera Panna','Heera Panna'),
    ('Maheshwari Chowk','Maheshwari Chowk'),
    ('Mhada','Mhada'),
    ('Qureshi Compound','Qureshi Compound'),
    ('Roshan Nagar','Roshan Nagar'),
    ('Santosh Nagar','Santosh Nagar'),
    ('Serenity','Serenity'),
    ('Shakti Nagar','Shakti Nagar'),
    ('Tarapore Garden','Tarapore Garden'),
    ('Tarapore Towers','Tarapore Towers'),
    ('Walawalkar','Walawalkar')

]
EmployeePost = [
    ('Driver','Driver'),
    ('Sweeper','Sweeper'),
    
]

class GarbageSegForm(forms.ModelForm):
    
    coll_date = forms.DateField(label = _(u'Date'),widget=forms.TextInput(attrs={'type': 'date'}),initial=datetime.date.today)
    # zone_id = forms.IntegerField(widget=forms.HiddenInput())
    region_name = forms.CharField(max_length=100)
    wet_waste_bf = forms.FloatField(label='Wet waste in kg')  # Field renamed to remove unsuitable characters.
    dry_waste_bf = forms.FloatField(label='Dry waste in kg')  # Field renamed to remove unsuitable characters.
    hazardous_waste = forms.FloatField(label='Hazardous waste in kg')  # Field renamed to remove unsuitable characters.
    # landfill_surrounding = forms.FloatField(label='landfill surrounding')  # Field renamed to remove unsuitable characters.
    recyclable_waste = forms.FloatField(label='Recyclable waste')  # Field renamed to remove unsuitable characters.
    compostable_waste = forms.FloatField(label = 'Compostable waste')
    building_name = forms.CharField(label = 'Building Name')

    class Meta:

        model = Report
        fields = '__all__'
        # exclude = ['zone_id','reason_late_entry']

class GrievanceForm(forms.ModelForm):
    YESNO_CHOICES = ((0, 'No'), (1, 'Yes'))
    name= forms.CharField(label = _(u'Name'))
    email = forms.CharField(label = _(u'email'))
    mobile = forms.IntegerField(label = _(u'mobile'))
    grievance = forms.CharField(widget=forms.Textarea(attrs={"rows":15, "cols":50}),label = _(u'grievance'))
    # grievance_no = forms.CharField(widget=forms.HiddenInput(),label = _(u'grievance no'))
    audio_src = forms.CharField(widget=forms.HiddenInput(),required=False)
    img_src = forms.CharField(widget=forms.HiddenInput(),required=False)
    # grievance_no = forms.CharField(widget=forms.HiddenInput())
  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Grievance
        fields = '__all__'
        # exclude = ['latitude','longitude','id','audio_src','img_src']
        widgets = {'audio_src':forms.HiddenInput(),'img_src':forms.HiddenInput(),'grievance_no':forms.HiddenInput()}

class Ward61BuildingsOsm2Nov2021Form(forms.ModelForm): 
    # geom = forms.CharField(label = _(u'Geometry'))  # This field type is a guess.
    # fid = forms.IntegerField(label = _(u'FId'))
    # osm_id = forms.DecimalField(label = _(u'OSM ID'))
    addrstreet = forms.CharField(label = _(u'Address'),required=False)
    building_type = forms.CharField(label = _(u'Building Type'),required=False)
    building_name = forms.CharField(label = _(u'Building Name'))
    num_flat = forms.IntegerField(label = _(u'Number of Flats'))
    num_shops = forms.IntegerField(label = _(u'Number of Shops'),required=False)
    num_floors = forms.IntegerField(label = _(u'Number of Floors'),required=False)
    wing_name = forms.CharField(label = _(u'Wing Name'),required=False)
    region = forms.CharField(label = _(u'Region'))
    councillor_ward = forms.CharField(label = _(u'Councillor Ward'),required=False)
    admin_ward = forms.CharField(label = _(u'Admin Ward'),required=False)
    # def __str__(self):
    #     return str(self.name)
    def clean(self):
        cleaned_data = self.cleaned_data
        num_flat = cleaned_data.get('num_flat')
        wing_name = cleaned_data.get('wing_name')
        if not any([num_flat, wing_name]):
            raise forms.ValidationError(u'Please enter Name of the Wing')
            # raise forms.ValidationError('Future Dates are not allowed.!!')
        
    class Meta:
        model = Ward61BuildingsOsm2Nov2021
        fields = '__all__'
        exclude = ['geom','roofmateri','osm_id']

class MumbaiBuildingsWardPrabhagwise17JanForm(forms.ModelForm): 
    # geom = forms.CharField(label = _(u'Geometry'))  # This field type is a guess.
    # fid = forms.IntegerField(label = _(u'FId'))
    # osm_id = forms.DecimalField(label = _(u'OSM ID'))
    address = forms.CharField(label = _(u'Address'),required=False)
    building_type = forms.CharField(label = _(u'Building Type'),required=False)
    building_name = forms.CharField(label = _(u'Building Name'))
    num_flat = forms.IntegerField(label = _(u'Number of Flats'),required=False)
    num_shops = forms.IntegerField(label = _(u'Number of Shops'),required=False)
    num_floors = forms.IntegerField(label = _(u'Number of Floors'),required=False)
    wing_name = forms.CharField(label = _(u'Wing Name'),required=False)
    region = forms.CharField(label = _(u'Region'),required=False)
    village = forms.CharField(label = _(u'Village'),required=False)

    validity = forms.CharField(label = _(u'Validity'),required=False)
    updated_by = forms.CharField(label = _(u'Updated By'))
    update_time = forms.CharField(label = _(u'Update Time'))
    device_ip = forms.CharField(label = _(u'Device IP'),required=False)

    
    def clean(self):
        cleaned_data = self.cleaned_data
   
        
    class Meta:
        model = MumbaiBuildingsWardPrabhagwise17Jan
        fields = '__all__'
        exclude = ['geom','wkt','building_i','sac_number','sac_type','before_geo','id1','prabhag_no','description','fid','district','ward_id','ward_name_field','mcgm_usern','mcgm_updat','prop_add']

class WasteSegregationDetailsForm(forms.ModelForm): 
    coll_date  = forms.DateField(label = _(u'Date'),widget=forms.TextInput(attrs={'type': 'date'}),initial=datetime.date.today)
    # region = forms.ModelChoiceField(queryset = WasteSegregationDetails.objects.filter(region__isnull=False).values_list('region', flat=True).distinct('region'),empty_label="(Nothing)")
    # region = forms.ModelChoiceField(label = _(u'Region Name'),queryset = WasteSegregationDetails.objects.all(),empty_label="(Choose Region)", to_field_name="region")
    region = forms.ModelChoiceField(label = _(u'Region Name'),queryset =WasteSegregationDetails.objects.all(),to_field_name='region', required=False)
    # building_cluster = forms.CharField(label = _(u'Building Name'),building_choices,widget=forms.Select())
    building_name = forms.ModelChoiceField(label = _(u'Building Name'),queryset = WasteSegregationDetails.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}))

    # category = forms.ModelChoiceField(label = _(u'Building Category'),max_length=100)
    num_wings = forms.IntegerField(label=_(u'Number of Wings'))
    wing_name = forms.CharField(max_length=100)
    building_type = forms.ModelChoiceField(label = _(u'Building Type'),queryset = WasteSegregationDetails.objects.all(),to_field_name='building_type',required=False)
    # building_type = forms.CharField(label = _(u'Building Type'))
    population = forms.IntegerField(label=_(u'Building Population'))
    num_households_premises = forms.IntegerField(label=_(u'Number of households'))
    num_shops_premises = forms.IntegerField(label=_(u'Number of Shops'))
    type_waste_generator = forms.CharField(label = _(u'Type of waste generator'),max_length=100)
    waste_segregation = forms.CharField(label = _(u'Is segregation done'),max_length=100)
    wet_waste_before_segregation = forms.IntegerField(label=_(u'Wet Waste before Segregation (in Kgs)'))
    dry_waste_before_segregation = forms.IntegerField(label=_(u'Dry Waste before Segregation (in Kgs)'))
    hazardous_waste = forms.IntegerField(label=_(u'Hazardous Waste before Segregation (in Kgs)'))
    compostable_waste = forms.IntegerField(label=_(u'Compostable Waste before Segregation (in Kgs)'))
    recyclable_waste = forms.IntegerField(label=_(u'Recyclable Waste before Segregation (in Kgs)'))
    rejected_waste = forms.IntegerField(label=_(u'Rejected Waste before Segregation (in Kgs)'))
    composting_type = forms.CharField(label = _(u'Composting Type'),max_length=100)
    compost_bin_by_mcgm = forms.CharField(label = _(u'Bin provided by MCGM'),max_length=100)
    date_notice_issued = forms.DateField(label=_(u'Date of Notice Issued'),widget=forms.TextInput(attrs={'type': 'date'}),initial=datetime.date.today)
    name_number = forms.CharField(label=_(u'Name and Mobile number of Building Secretaty/Incharge'),max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['region'].queryset=WasteSegregationDetails.objects.filter(region__isnull=False).values_list('region', flat=True).distinct('region')
        # self.fields['building_cluster'].queryset=WasteSegregationDetails.objects.values_list('building_cluster', flat=True).distinct('building_cluster')
        self.fields['building_name'].queryset=WasteSegregationDetails.objects.filter(region=self.data.get('region'))
        self.fields['building_type'].queryset=WasteSegregationDetails.objects.filter(building_type__isnull=False).values_list('building_type', flat=True).distinct('building_type')
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['building_name'].queryset = WasteSegregationDetails.objects.filter(region=region_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['building_cluster'].queryset = self.instance.country.city_set.order_by('name')
        
    class Meta:
        model = WasteSegregationDetails
        fields = '__all__'
        # fields = ['region','building_name']
        exclude = ['category']

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email",'role','designation','area','Ward','prabhag', "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class EmployeeDetailsForm(forms.ModelForm): 
    #adminward =forms.CharField(label = _(u'Admin Ward'),max_length=50)
    councillorward = forms.CharField(label=_(u'Councillor Ward (Prabhag) '),max_length=100,widget=forms.Select(choices=councillorWard))
    region = forms.CharField(label = _(u'Region Name'),widget=forms.Select(choices=Regions))
    emp_category =forms.CharField(label = _(u'Scavenger'),widget=forms.Select(choices=EmployeePost))
    emp_name =forms.CharField(label = _(u'Employee Name'),max_length = 100)
    emp_mobile =forms.IntegerField(label = _(u'Employee Mobile No.'))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = EmployeeDetails
        fields = '__all__'
        # exclude =['emp_id']
        
        
class WasteSegregationDetailsRevised2march22Form(forms.ModelForm): 
    coll_date  = forms.DateField(label = _(u'Date'),widget=forms.TextInput(attrs={'type': 'date'}),initial=datetime.date.today)
    # # region = forms.ModelChoiceField(queryset = WasteSegregationDetails.objects.filter(region__isnull=False).values_list('region', flat=True).distinct('region'),empty_label="(Nothing)")
    # # region = forms.ModelChoiceField(label = _(u'Region Name'),queryset = WasteSegregationDetails.objects.all(),empty_label="(Choose Region)", to_field_name="region")
    # region = forms.ModelChoiceField(label = _(u'Region Name'),queryset =WasteSegregationDetails.objects.all(),to_field_name='region', required=False)
    # # building_cluster = forms.CharField(label = _(u'Building Name'),building_choices,widget=forms.Select())
    # building_name = forms.ModelChoiceField(label = _(u'Building Name'),queryset = WasteSegregationDetails.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}))

    # # category = forms.ModelChoiceField(label = _(u'Building Category'),max_length=100)
    # num_wings = forms.IntegerField(label=_(u'Number of Wings'))
    # wing_name = forms.CharField(max_length=100)
    # building_type = forms.ModelChoiceField(label = _(u'Building Type'),queryset = WasteSegregationDetails.objects.all(),to_field_name='building_type',required=False)
    # # building_type = forms.CharField(label = _(u'Building Type'))
    # population = forms.IntegerField(label=_(u'Building Population'))
    # num_households_premises = forms.IntegerField(label=_(u'Number of households'))
    # num_shops_premises = forms.IntegerField(label=_(u'Number of Shops'))
    # type_waste_generator = forms.CharField(label = _(u'Type of waste generator'),max_length=100)
    # waste_segregation = forms.CharField(label = _(u'Is segregation done'),max_length=100)
    # wet_waste_before_segregation = forms.IntegerField(label=_(u'Wet Waste before Segregation (in Kgs)'))
    # dry_waste_before_segregation = forms.IntegerField(label=_(u'Dry Waste before Segregation (in Kgs)'))
    # hazardous_waste = forms.IntegerField(label=_(u'Hazardous Waste before Segregation (in Kgs)'))
    # compostable_waste = forms.IntegerField(label=_(u'Compostable Waste before Segregation (in Kgs)'))
    # recyclable_waste = forms.IntegerField(label=_(u'Recyclable Waste before Segregation (in Kgs)'))
    # rejected_waste = forms.IntegerField(label=_(u'Rejected Waste before Segregation (in Kgs)'))
    # composting_type = forms.CharField(label = _(u'Composting Type'),max_length=100)
    # compost_bin_by_mcgm = forms.CharField(label = _(u'Bin provided by MCGM'),max_length=100)
    # date_notice_issued = forms.DateField(label=_(u'Date of Notice Issued'),widget=forms.TextInput(attrs={'type': 'date'}),initial=datetime.date.today)
    # name_number = forms.CharField(label=_(u'Name and Mobile number of Building Secretaty/Incharge'),max_length=100)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['region'].queryset=WasteSegregationDetails.objects.filter(region__isnull=False).values_list('region', flat=True).distinct('region')
    #     # self.fields['building_cluster'].queryset=WasteSegregationDetails.objects.values_list('building_cluster', flat=True).distinct('building_cluster')
    #     self.fields['building_name'].queryset=WasteSegregationDetails.objects.filter(region=self.data.get('region'))
    #     self.fields['building_type'].queryset=WasteSegregationDetails.objects.filter(building_type__isnull=False).values_list('building_type', flat=True).distinct('building_type')
    #     if 'region' in self.data:
    #         try:
    #             region_id = int(self.data.get('region'))
    #             self.fields['building_name'].queryset = WasteSegregationDetails.objects.filter(region=region_id)
    #         except (ValueError, TypeError):
    #             pass  # invalid input from the client; ignore and fallback to empty City queryset
    #     # elif self.instance.pk:
    #     #     self.fields['building_cluster'].queryset = self.instance.country.city_set.order_by('name')
        
    class Meta:
        model = WasteSegregationDetailsRevised2March22
        fields = '__all__'
        # fields = ['region','building_name']
        # exclude = ['id']
