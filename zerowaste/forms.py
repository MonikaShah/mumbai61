from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Report,Grievance,WasteSegregationDetails#,OsmBuildings29Oct21
from map.models import Ward61BuildingsOsm2Nov2021
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, ButtonHolder
import datetime
# from phonenumber_field.formfields import PhoneNumberField
from django.contrib.gis import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from datetime import timedelta
# import pandas as pd
# import numpy as np
import xlrd
import csv

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


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Grievance
        fields = '__all__'
        # exclude = ['latitude','longitude','id','audio_src','img_src']
        # widgets = {'selectzones': forms.HiddenInput(),'selectlanes':forms.HiddenInput()}

class Ward61BuildingsOsm2Nov2021Form(forms.ModelForm): 
    # geom = forms.CharField(label = _(u'Geometry'))  # This field type is a guess.
    # fid = forms.IntegerField(label = _(u'FId'))
    # osm_id = forms.DecimalField(label = _(u'OSM ID'))
    addrstreet = forms.CharField(label = _(u'Address'))
    building = forms.CharField(label = _(u'Building Type'))
    name = forms.CharField(label = _(u'Name'))
    num_flat = forms.IntegerField(label = _(u'Number of Flats'))
    wing = forms.IntegerField(label = _(u'Wing'))
    region = forms.CharField(label = _(u'Region'))
    # def __str__(self):
    #     return str(self.name)
    def clean(self):
        cleaned_data = self.cleaned_data
        num_flat = cleaned_data.get('num_flat')
        wing = cleaned_data.get('wing')
        if not any([num_flat, wing]):
            raise forms.ValidationError(u'Please enter a value')
            # raise forms.ValidationError('Future Dates are not allowed.!!')
        
    class Meta:
        model = Ward61BuildingsOsm2Nov2021
        fields = '__all__'
        exclude = ['geom','roofmateri','osm_id']

class WasteSegregationDetailsForm(forms.ModelForm): 
    coll_date  = forms.DateField(label = _(u'Date'),widget=forms.TextInput(attrs={'type': 'date'}),initial=datetime.date.today)
    # region = forms.ModelChoiceField(queryset = WasteSegregationDetails.objects.filter(region__isnull=False).values_list('region', flat=True).distinct('region'),empty_label="(Nothing)")
    # region = forms.ModelChoiceField(label = _(u'Region Name'),queryset = WasteSegregationDetails.objects.all(),empty_label="(Choose Region)", to_field_name="region")
    region = forms.ModelChoiceField(label = _(u'Region Name'),queryset =WasteSegregationDetails.objects.all(),to_field_name='region', required=False)
    # building_cluster = forms.CharField(label = _(u'Building Name'),building_choices,widget=forms.Select())
    building_cluster = forms.ModelChoiceField(label = _(u'Building Name'),queryset = WasteSegregationDetails.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}))

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
        self.fields['building_cluster'].queryset=WasteSegregationDetails.objects.filter(region=self.data.get('region'))
        self.fields['building_type'].queryset=WasteSegregationDetails.objects.filter(building_type__isnull=False).values_list('building_type', flat=True).distinct('building_type')
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['building_cluster'].queryset = WasteSegregationDetails.objects.filter(region=region_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['building_cluster'].queryset = self.instance.country.city_set.order_by('name')
        
    class Meta:
        model = WasteSegregationDetails
        fields = '__all__'
        # fields = ['region','building_cluster']
        exclude = ['category']

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user