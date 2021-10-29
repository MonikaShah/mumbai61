from django import forms
from .models import Report,Grievance,OsmBuildings29Oct21
import os
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

class OsmBuildings29Oct21Form(forms.ModelForm): 
    # geom = forms.CharField(label = _(u'Geometry'))  # This field type is a guess.
    # fid = forms.IntegerField(label = _(u'FId'))
    # osm_id = forms.FloatField(label = _(u'OSM ID'))
    addrstreet = forms.CharField(label = _(u'Address'))
    building = forms.CharField(label = _(u'Building Type'))
    name = forms.CharField(label = _(u'Name'))
    num_flats = forms.IntegerField(label = _(u'Number of Flats'))
    wings = forms.IntegerField(label = _(u'Wing'))
    region = forms.CharField(label = _(u'Region'))
    class Meta:

        model = OsmBuildings29Oct21
        fields = '__all__'
        exclude = ['geom','osm_id','fid']