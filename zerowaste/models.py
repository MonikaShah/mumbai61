# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from map.models import *
from django.core.validators import MinLengthValidator, int_list_validator

# from django.contrib.gis.db import models
class CustomAccountManager(BaseUserManager):
    def create_superuser(self, username, password, **other_fields):
        default_ward = MumbaiWardBoundary2Jan2022.objects.get(id=1)
        default_prabhag = MumbaiPrabhagBoundaries3Jan2022V2.objects.get(id=1)

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('area','Ward')
        other_fields.setdefault('designation','superuser')
        other_fields.setdefault('Ward', default_ward)
        other_fields.setdefault('prabhag', default_prabhag)
        
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(username,password,**other_fields)

    def create_user(self, username,password,**other_fields):

        # print(prabhag,Ward)
        user = self.model(username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user

level = (('Select','none'),('Ward','Ward'),('Prabhag','Prabhag'))
role_list = (('Select','none'),('CT','Citizen'),('MO','Municipality Officer'),('SR','Society Representative'),('SV','Student Volunteer'))
class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(null=True,blank=True)
    role = models.CharField(max_length=9,
                  choices=role_list,
                  default='none')
    designation = models.CharField(max_length=150,null=True,blank=True )
    area = models.CharField(max_length=9,
                  choices=level,
                  default='none')
    Ward = models.ForeignKey(MumbaiWardBoundary2Jan2022,to_field='ward_id', on_delete=models.SET_NULL, null=True,default=0,blank=True)
    prabhag = models.ForeignKey(MumbaiPrabhagBoundaries3Jan2022V2,to_field='prabhag_no', on_delete=models.SET_NULL, null=True,default=0,blank=True)
    is_staff = models.BooleanField(default=False,null=True,blank=True)
    is_active = models.BooleanField(default=True,null=True,blank=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['first_name]

    def __str__(self):
        return self.username
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    

    class Meta:
        managed = False
        db_table = 'zerowaste_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Report(models.Model):
    # report_id = models.AutoField(primary_key=True)
    coll_date = models.DateField()
    # zone_id = models.IntegerField()
    region_name = models.CharField(max_length=100, default = "region A")
    building_name = models.CharField(max_length=100, default = "A")
    # region_name = models.CharField(max_length=100, default = "staff Hostel")
    wet_waste_bf = models.FloatField(db_column='wet_waste_bf', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    dry_waste_bf = models.FloatField(db_column='dry_waste_bf', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    hazardous_waste = models.FloatField(db_column='hazardous_waste', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    # landfill_surrounding = models.FloatField(db_column='landfill surrounding', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    recyclable_waste = models.FloatField(db_column='recyclable_waste', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    compostable_waste = models.FloatField(db_column='compostable_waste', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    rejected_waste = models.FloatField(db_column='rejected_waste',blank=True,null=True)
    # class Meta:
    #     managed = False
    #     db_table = 'report'

    def __str__(self):
        return self.coll_date

class Grievance(models.Model):
    name = models.CharField(max_length=100,help_text=_('Name'))
    email = models.EmailField(blank=True)
    mobile = models.CharField(max_length=15,blank=True, null=True)
    # selectzones = models.CharField(max_length=100)
    # selectlanes = models.CharField(max_length=100)
    # audio_src = models.CharField(max_length=100)
    audio_src = models.CharField(max_length=100,null=True, default=None, blank=True)
    # img_src =  models.CharField(max_length=100)
    img_src =  models.CharField(max_length=100,null=True, default=None, blank=True)
    grievance = models.TextField(blank=True, null=False, default='Testing')
    # grievance = models.TextField(null=True, default=None, blank=True),
    uploaded_at = models.DateTimeField(auto_now_add=True)
    grievance_no = models.CharField(max_length=100,null=True, default=None, blank=True)

    class Meta:
        managed = True
        db_table = 'grievance'
    def __str__(self):
        return self.email

class Rating(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(null=True,max_length=10)
    email = models.CharField(max_length=100,null=True)
    service_swk = models.IntegerField(default='yes')
    timing_swk = models.IntegerField(null=True)
    mobile_swk = models.IntegerField(null=True)
    compost_kit_garden = models.IntegerField(null=True)
    communicate_swk = models.IntegerField(null=True)
    solid_waste_man = models.IntegerField(null=True)
    service_workers = models.IntegerField(null=True)
    segregation = models.IntegerField(null=True)
    recycle_process = models.IntegerField(null=True)
    awareness = models.IntegerField(null=True)
    role = models.CharField(max_length=10)


class WasteSegregationDetails(models.Model):
    track_id = models.IntegerField(blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    building_name = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    num_wings = models.CharField(max_length=100, blank=True, null=True)
    wing_name = models.CharField(max_length=100, blank=True, null=True)
    building_type = models.CharField(max_length=100, blank=True, null=True)
    population = models.CharField(max_length=100, blank=True, null=True)
    num_households_premises = models.CharField(max_length=100, blank=True, null=True)
    num_shops_premises = models.CharField(max_length=100, blank=True, null=True)
    type_waste_generator = models.CharField(max_length=100, blank=True, null=True)
    waste_segregation = models.CharField(max_length=100, blank=True, null=True)
    wet_waste_before_segregation = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    dry_waste_before_segregation = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    hazardous_waste = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    compostable_waste = models.CharField(max_length=100, blank=True, null=True)
    recyclable_waste = models.CharField(max_length=100, blank=True, null=True)
    rejected_waste = models.CharField(max_length=100, blank=True, null=True)
    composting_type = models.CharField(max_length=100, blank=True, null=True)
    compost_bin_by_mcgm = models.CharField(max_length=100, blank=True, null=True)
    date_notice_issued = models.CharField(max_length=100, blank=True, null=True)
    name_number = models.CharField(max_length=100, blank=True, null=True)
    coll_date = models.DateField(blank=True, null=True)
    building_bifurcation = models.CharField(max_length=50, blank=True, null=True)
    admin_ward = models.CharField(max_length=50, blank=True, null=True)
    councillor_ward = models.CharField(max_length=50, blank=True, null=True)
    ward = models.CharField(default = '61',max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'waste_segregation_details'


class EmployeeDetails(models.Model):
    # emp_id = models.AutoField(primary_key=True)
    # ward =models.CharField(max_length=50,default= 'K/W')
    ward =models.CharField(max_length=50)
    prabhag = models.CharField(max_length=100,blank=True, null=True)
    # prabhag = models.ForeignKey(MumbaiPrabhagBoundaries3Jan2022V2.objects.filter(ward_name__contains='K/W'))
    chowky = models.CharField(max_length=100)
    post =models.CharField(max_length = 100)
    name =models.CharField(max_length = 100)
    mobile = models.CharField(verbose_name="Phone number", max_length=10,validators=[int_list_validator(sep=''),MinLengthValidator(10),],default='1111111111')
    councillor = models.CharField(max_length = 100,null=True,blank=True)

    class Meta:
        managed = True
        db_table = 'employee_details'
        

    def __str__(self):
        return "Prabhag -"+self.prabhag + " " + self.post+ " "+ self.name

class HumanResourceData(models.Model):
    # emp_id = models.AutoField(primary_key=True)
    # ward =models.CharField(max_length=50,default='K/W')
    # ward =models.CharField(MumbaiPrabhagBoundaries3Jan2022V2.objects.values('ward_id_field'))
    # ward = models.ForeignKey(MumbaiWardBoundary2Jan2022,to_field='ward_id', on_delete=models.SET_NULL, null=True,default=0,blank=True)
    # prabhag = models.ForeignKey(MumbaiPrabhagBoundaries3Jan2022V2,to_field='prabhag_no', on_delete=models.SET_NULL, null=True,default=0,blank=True)
    ward =models.CharField(max_length=50)
    prabhag = models.CharField(max_length=100)
    # prabhag = models.ForeignKey(MumbaiPrabhagBoundaries3Jan2022V2.objects.filter(ward_name__contains='S'),on_delete=models.SET_NULL)
    # chowky = models.CharField(max_length=100)
    road_name = models.CharField(max_length=100)
    building_name = models.CharField(max_length=100)
    sac_no = models.IntegerField
    designation =models.CharField(max_length = 100)
    name_contact_person =models.CharField(max_length = 100)
    mobile_contact_person = models.CharField(verbose_name="Phone number", max_length=10,
    validators=[int_list_validator(sep=''),MinLengthValidator(10),], 
    default='1111111111')
    email_contact_person = models.EmailField(verbose_name="Email Id", max_length=50)
    

    class Meta:
        managed = True
        db_table = 'humanresourcedata'

    def __str__(self):
        return "Prabhag -"+self.prabhag + " " + self.designation+ " "+ self.name_contact_person

# class CensusTable(models.Model):
#     sstart = models.DateTimeField(blank=True, null=True)
#     eend = models.DateTimeField(blank=True, null=True)
#     name_of_the_city = models.CharField(max_length=50, blank=True, null=True)
#     cencus_code = models.IntegerField(blank=True, null=True)
#     tree_common_name = models.CharField(max_length=50, blank=True, null=True)
#     scientific_name = models.CharField(max_length=50, blank=True, null=True)
#     tree_type = models.CharField(max_length=50, blank=True, null=True)
#     tree_gps_location = models.CharField(max_length=50, blank=True, null=True)
#     tree_gps_location_latitude = models.CharField(max_length=30, blank=True, null=True)
#     tree_gps_location_longitude = models.CharField(max_length=30, blank=True, null=True)
#     tree_gps_location_altitude = models.CharField(max_length=30, blank=True, null=True)
#     tree_gps_location_precision = models.CharField(max_length=30, blank=True, null=True)
#     photo = models.CharField(max_length=70, blank=True, null=True)
#     photo_url = models.BinaryField(blank=True, null=True)
#     tree_girth_in_inches = models.IntegerField(blank=True, null=True)
#     tree_height_in_cm = models.IntegerField(blank=True, null=True)
#     tree_canopy = models.CharField(max_length=50, blank=True, null=True)
#     total_area_in_sq_kms_under_all_trees = models.IntegerField(blank=True, null=True)
#     total_area_in_sq_kms_under_native_indegeniuos_trees = models.IntegerField(blank=True, null=True)
#     current_tree_age = models.IntegerField(blank=True, null=True)
#     age_of_tree_when_planted = models.CharField(max_length=50, blank=True, null=True)
#     date_of_plantation = models.DateField(blank=True, null=True)
#     present_status_of_tree = models.CharField(max_length=50, blank=True, null=True)
#     tree_ownership_plantation_initiated_by = models.CharField(max_length=50, blank=True, null=True)
#     please_specify_tree_ownership = models.CharField(max_length=50, blank=True, null=True)
#     name_of_the_owner = models.CharField(max_length=50, blank=True, null=True)
#     field_version_field = models.CharField(db_column='__version__', max_length=50, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'. Field renamed because it ended with '_'.
#     tree_scientific_tree_local_name = models.CharField(max_length=50, blank=True, null=True)
#     address = models.CharField(max_length=50, blank=True, null=True)
#     id = models.BigIntegerField(primary_key=True)
#     field_uuid = models.CharField(db_column='_uuid', max_length=50, blank=True, null=True)  # Field renamed because it started with '_'.
#     field_submission_time = models.DateField(db_column='_submission_time', blank=True, null=True)  # Field renamed because it started with '_'.
#     field_validation_status = models.CharField(db_column='_validation_status', max_length=50, blank=True, null=True)  # Field renamed because it started with '_'.
#     field_notes = models.CharField(db_column='_notes', max_length=50, blank=True, null=True)  # Field renamed because it started with '_'.
#     field_status = models.CharField(db_column='_status', max_length=50, blank=True, null=True)  # Field renamed because it started with '_'.
#     field_submitted_by = models.CharField(db_column='_submitted_by', max_length=50, blank=True, null=True)  # Field renamed because it started with '_'.
#     field_tags = models.CharField(db_column='_tags', max_length=50, blank=True, null=True)  # Field renamed because it started with '_'.
#     field_index = models.IntegerField(db_column='_index', blank=True, null=True)  # Field renamed because it started with '_'.
#     tree_gps_location_geom = models.PointField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'census_table'
cluster = (('Yes','Yes'),('No','No'))

qual = (('Good','Good'),('Average','Average'),('Poor','Poor'))

class WasteSegregationDetailsRevised2March22(models.Model):
    ward = models.ForeignKey(MumbaiWardBoundary2Jan2022,to_field='ward_id', on_delete=models.SET_NULL, null=True,default=0,blank=True)
    prabhag = models.ForeignKey(MumbaiPrabhagBoundaries3Jan2022V2,to_field='prabhag_no', on_delete=models.SET_NULL, null=True,default=0,blank=True)
    road_name = models.CharField(max_length=254, blank=True, null=True)
    building_name = models.CharField(max_length=255, blank=True, null=True)
    sac_no = models.CharField(max_length=254, blank=True, null=True)
    building_type = models.CharField(max_length=255, blank=True, null=True)
    building_cluster = models.CharField(choices=cluster,default='No',max_length=255, blank=True, null=True)
    # cluster_name = models.CharField(max_length=255, blank=True, null=True)
    num_wings = models.CharField(max_length=255, blank=True, null=True)
    wing_name = models.CharField(max_length=255, blank=True, null=True)
    num_households_premises = models.CharField(max_length=255, blank=True, null=True)
    num_shops_premises = models.CharField(max_length=255, blank=True, null=True)
    approx_population = models.CharField(max_length=255, blank=True, null=True)
    seg_done = models.CharField(choices=cluster,default='No',max_length=255, blank=True, null=True)
    mixed_waste= models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    wet_waste = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dry_waste = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dom_waste =models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    e_waste =models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bulk_waste =models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    coll_date = models.DateField(blank=True, null=True)
    # username = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    username =  models.CharField(max_length=50,null=True)
    date_time =  models.DateTimeField(auto_now_add=True)
    # composting_status = models.CharField(choices=cluster,default='No',max_length=255, blank=True, null=True)
    # compostin

    class Meta:
        managed = True
        db_table = 'waste_segregation_details_revised_2march22'
    def __str__(self):
        # return "Prabhag -"+self.prabhag + " " +"Building Name -"+ self.building_name+ " "+ "Date -"+self.coll_date
        # return "Prabhag -"+str(self.prabhag) + " "+"Building Name -"+ self.building_name+self.coll_date.strftime("%b %d %Y")
        return "Prabhag -"+str(self.prabhag) + " "+"Building Name -"+ self.building_name+self.coll_date.strftime("%b %d %Y %H %M %S")


class PrimaryParentId(models.Model):
    geom = models.MultiPointField(blank=True, null=True)
    sac_number = models.CharField(max_length=254, blank=True, null=True)
    parent_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'primary_parent_id'
        
class compost_data(models.Model):
    ward = models.ForeignKey(MumbaiWardBoundary2Jan2022,to_field='ward_id', on_delete=models.SET_NULL, null=True,default=0,blank=True)
    prabhag_no = models.CharField(max_length=254, blank=True, null=True)
    sac_no = models.CharField(max_length=254, blank=True, null=True)
    road_name = models.CharField(max_length=254, blank=True, null=True)   
    building_name = models.CharField(max_length=255, blank=True, null=True)
    compost_weight = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    testing_done = models.CharField(choices=cluster,default='No',max_length=255, blank=True, null=True)
    compost_quality = models.CharField(choices=qual, default='Average',max_length=255, blank=True,null=True)
    coll_date = models.DateField(blank=True, null=True)
    username =  models.CharField(max_length=50,null=True)
    
    class Meta:
        managed = True
        db_table = 'compost_data'

    def __str__(self):
        return "Prabhag -"+str(self.prabhag_no) + " "+"Building Name -"+ self.building_name+" Date -"+self.coll_date


# class BuildingsWardWise4March(models.Model):
#     building_id = models.IntegerField()
#     ward_name = models.CharField(max_length=50, blank=True, null=True)
#     ward_id = models.CharField(max_length=50, blank=True, null=True)
#     prabhag_no = models.CharField(max_length=50, blank=True, null=True)
#     building_name = models.CharField(max_length=250, blank=True, null=True)
#     road_name = models.CharField(max_length=250, blank=True, null=True)
#     name_jo = models.CharField(max_length=250, blank=True, null=True)
#     section = models.CharField(max_length=230, blank=True, null=True)
#     building_type = models.CharField(max_length=30, blank=True, null=True)
#     dry = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
#     wet = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
#     cluster_name = models.CharField(max_length=270, blank=True, null=True)
#     building_cluster = models.CharField(max_length=270, blank=True, null=True)
#     no_of_house = models.IntegerField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'buildings_ward_wise_4march'
class BuildingsWard9April22(models.Model):
    building_id = models.IntegerField(blank=True, null=True)
    ward_name = models.CharField(max_length=50, blank=True, null=True)
    ward_id = models.CharField(max_length=50, blank=True, null=True)
    prabhag_no = models.CharField(max_length=50, blank=True, null=True)
    building_name = models.CharField(max_length=250, blank=True, null=True)
    road_segment = models.CharField(max_length=250, blank=True, null=True)
    name_jo = models.CharField(max_length=250, blank=True, null=True)
    section = models.CharField(max_length=230, blank=True, null=True)
    building_type = models.CharField(max_length=30, blank=True, null=True)
    dry = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    wet = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cluster_name = models.CharField(max_length=270, blank=True, null=True)
    building_cluster = models.CharField(max_length=270, blank=True, null=True)
    no_of_house = models.IntegerField(blank=True, null=True)
    road_name = models.CharField(max_length=250, blank=True, null=True)
    sac_no = models.CharField(max_length=250, blank=True, null=True)
    lat = models.CharField(max_length=250, blank=True, null=True)
    lng = models.CharField(max_length=250, blank=True, null=True)
    road_name_alias = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'buildings_ward_8april_22'
class KWestBeat22Jan(models.Model):
    geom = models.MultiLineStringField(blank=True, null=True)
    fid = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    descriptio = models.CharField(max_length=254, blank=True, null=True)
    length = models.CharField(max_length=254, blank=True, null=True)
    buffer = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'k_west_beat_22jan'


class BuildingUnder30Mtr(models.Model):
    uid = models.IntegerField(primary_key=True)
    geom = models.MultiPointField(blank=True, null=True)
    wkt = models.CharField(max_length=255, blank=True, null=True)
    building_i = models.CharField(max_length=255, blank=True, null=True)
    sac_number = models.CharField(max_length=255, blank=True, null=True)
    mcgm_usern = models.CharField(max_length=255, blank=True, null=True)
    mcgm_updat = models.CharField(max_length=255, blank=True, null=True)
    sac_type = models.CharField(max_length=255, blank=True, null=True)
    wing_name = models.CharField(max_length=255, blank=True, null=True)
    num_flat = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    num_shops = models.CharField(max_length=255, blank=True, null=True)
    num_floors = models.CharField(max_length=255, blank=True, null=True)
    building_name = models.CharField(max_length=255, blank=True, null=True)
    building_type = models.CharField(max_length=255, blank=True, null=True)
    village = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    before_geo = models.CharField(max_length=254, blank=True, null=True)
    id1 = models.BigIntegerField(blank=True, null=True)
    prabhag_no = models.CharField(max_length=254, blank=True, null=True)
    fid = models.IntegerField(blank=True, null=True)
    district = models.CharField(max_length=254, blank=True, null=True)
    ward_id_2 = models.CharField(max_length=254, blank=True, null=True)
    ward_name_field = models.CharField(db_column='ward_name_', max_length=254, blank=True, null=True)  # Field renamed because it ended with '_'.
    id = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    prop_add = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    device_ip = models.CharField(max_length=255, blank=True, null=True)
    validity = models.BooleanField(blank=True, null=True)
    id_2 = models.BigIntegerField(blank=True, null=True)
    fid_2 = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    descriptio = models.CharField(max_length=254, blank=True, null=True)
    length = models.CharField(max_length=254, blank=True, null=True)
    buffer = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'building_under_30mtr'

# class MergedBuildings5Sept22(models.Model):
#     id=models.IntegerField(primary_key=True)
#     geom = models.MultiPointField(blank=True, null=True)
#     mcgm_usern = models.CharField(max_length=254, blank=True, null=True)
#     mcgm_updat = models.CharField(max_length=254, blank=True, null=True)
#     ward_name_field = models.CharField(db_column='ward_name_', max_length=254, blank=True, null=True)  # Field renamed because it ended with '_'.
#     ward_id_2 = models.CharField(max_length=254, blank=True, null=True)
#     prabhag_no = models.CharField(max_length=254, blank=True, null=True)
#     building_n = models.CharField(max_length=254, blank=True, null=True)
#     building_t = models.CharField(max_length=254, blank=True, null=True)
#     wing_name = models.CharField(max_length=254, blank=True, null=True)
#     num_flat = models.CharField(max_length=254, blank=True, null=True)
#     num_shops = models.CharField(max_length=254, blank=True, null=True)
#     num_floors = models.CharField(max_length=254, blank=True, null=True)
#     dry_waste = models.FloatField(blank=True, null=True)
#     wet_waste = models.FloatField(blank=True, null=True)
#     photo = models.CharField(max_length=80, blank=True, null=True)
#     wkt = models.CharField(max_length=254, blank=True, null=True)
#     building_i = models.CharField(max_length=254, blank=True, null=True)
#     sac_number = models.CharField(max_length=254, blank=True, null=True)
#     sac_type = models.CharField(max_length=254, blank=True, null=True)
#     district = models.CharField(max_length=254, blank=True, null=True)
#     prop_add = models.CharField(max_length=254, blank=True, null=True)
#     spot_id = models.BigIntegerField(blank=True, null=True)
#     road_name = models.CharField(max_length=80, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'Merged_buildings_5Sept22'

# class P122Buildings10October22(models.Model):
#     geom = models.MultiPointField(blank=True, null=True)
#     fid = models.BigIntegerField(blank=True, null=True)
#     sac_number = models.CharField(max_length=254, blank=True, null=True)
#     wing_name = models.CharField(max_length=254, blank=True, null=True)
#     num_flat = models.CharField(max_length=254, blank=True, null=True)
#     num_shops = models.CharField(max_length=254, blank=True, null=True)
#     num_floors = models.CharField(max_length=254, blank=True, null=True)
#     building_n = models.CharField(max_length=254, blank=True, null=True)
#     building_t = models.CharField(max_length=254, blank=True, null=True)
#     prabhag_no = models.CharField(max_length=254, blank=True, null=True)
#     ward_name_field = models.CharField(db_column='ward_name_', max_length=254, blank=True, null=True)  # Field renamed because it ended with '_'.
#     prop_add = models.CharField(max_length=254, blank=True, null=True)
#     cluster = models.CharField(max_length=20, blank=True, null=True)
#     clust_nm = models.CharField(max_length=50, blank=True, null=True)
#     population = models.BigIntegerField(blank=True, null=True)
#     bin_photo = models.CharField(max_length=100, blank=True, null=True)
#     username = models.CharField(max_length=50, blank=True, null=True)
#     date_time = models.CharField(max_length=100, blank=True, null=True)
#     email = models.CharField(max_length=50, blank=True, null=True)
#     qfield_username = models.CharField(max_length=50, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'P122_buildings_10october22'


class P122Buildings14October22(models.Model):
    geom = models.MultiPointField(blank=True, null=True)
    fid = models.BigIntegerField(blank=True, null=True)
    sac_number = models.CharField(max_length=254, blank=True, null=True)
    wing_name = models.CharField(max_length=254, blank=True, null=True)
    num_flat = models.CharField(max_length=254, blank=True, null=True)
    num_shops = models.CharField(max_length=254, blank=True, null=True)
    num_floors = models.CharField(max_length=254, blank=True, null=True)
    building_n = models.CharField(max_length=254, blank=True, null=True)
    building_t = models.CharField(max_length=254, blank=True, null=True)
    prabhag_no = models.CharField(max_length=254, blank=True, null=True)
    ward_name_field = models.CharField(db_column='ward_name_', max_length=254, blank=True, null=True)  # Field renamed because it ended with '_'.
    prop_add = models.CharField(max_length=254, blank=True, null=True)
    cluster = models.CharField(max_length=20, blank=True, null=True)
    clust_nm = models.CharField(max_length=50, blank=True, null=True)
    population = models.BigIntegerField(blank=True, null=True)
    bin_photo = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    date_time = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    qfield_username = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'p122_buildings_14october22'

class P122Buildings8Nov22(models.Model):
    fid = models.CharField(max_length=100, blank=True, null=True)
    sac_number = models.CharField(max_length=100, blank=True, null=True)
    wing_name = models.CharField(max_length=100, blank=True, null=True)
    num_flat = models.CharField(max_length=100, blank=True, null=True)
    num_shops = models.CharField(max_length=100, blank=True, null=True)
    num_floors = models.CharField(max_length=100, blank=True, null=True)
    building_n = models.CharField(max_length=100, blank=True, null=True)
    building_t = models.CharField(max_length=100, blank=True, null=True)
    prabhag_no = models.CharField(max_length=100, blank=True, null=True)
    ward_name_field = models.CharField(db_column='ward_name_', max_length=100, blank=True, null=True)  # Field renamed because it ended with '_'.
    prop_add = models.CharField(max_length=100, blank=True, null=True)
    cluster = models.CharField(max_length=100, blank=True, null=True)
    clust_nm = models.CharField(max_length=100, blank=True, null=True)
    population = models.CharField(max_length=100, blank=True, null=True)
    bin_photo = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    date_time = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    qfield_username = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'p122_buildings_8Nov22'

#student registration model
class data_form(models.Model):

    # id = models.IntegerField(primary_key=True) -- It throws an error because postgresql has an property that it generates id automatically, make primary key false
    emailF = models.CharField(max_length=100)
    studentName = models.CharField(max_length=100)
    age = models.CharField(max_length=3)
    collegeName = models.CharField(max_length=100)
    websiteUsername = models.CharField(max_length=100)
    sponsered = models.CharField(max_length=3)
    sponsBy = models.CharField(max_length=100)
    ownDevice = models.CharField(max_length=3)
    date = models.CharField(max_length=20)
    # grad_year= models.CharField(max_length=20)
    # grad_stream= models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'student_registration'

    def __str__(self):
        return self.websiteUsername+"- of - "+self.collegeName+" -Institute"
    

class links(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=100)
    class Meta:
        managed = True
        db_table = 'dashboard_links' 
    def __str__(self):
        return self.title
    
grpChoice = (('ESG','ESG'),('SWM','SWM'),('BMC','BMC'),('Startups','Startups'))    
class image_up(models.Model):
    
    # diet=models.OneToOneField(dietrecallmodel, on_delete=models.CASCADE)
    title=models.CharField( max_length=150,null=True)
    image = models.ImageField( upload_to='images/%Y/%m/%d')
    
class document_up(models.Model):
    grp =models.TextField(choices=grpChoice,default='SWM',null=True)
    title=models.CharField( max_length=150,null=True)
    Document = models.FileField(upload_to='documents/%Y/%m/%d')
    class Meta:
        managed =True
        db_table = 'resources_document'
    def __str__(self):
        return self.title
    
class ReportData(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    report = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(max_length=50, blank=True, null=True)
    # id = models.DecimalField(primary_key=True, max_digits=65535, decimal_places=65535)

    class Meta:
        managed = False
        db_table = 'report_data'

aggreCateChoice = (('Kabadi','Newspaper, Metal, Cardboxes, plastic, tins, wires etc.'),('bioHazardous','BioHazardous'),('cloth','Cloth/Chindi'),('furniture','Furniture'))
class AggregatorData(models.Model):
    shop_name=models.CharField(max_length=50, blank=True, null=True)
    owner_name = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.IntegerField(blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    aggr_category =models.TextField(choices=aggreCateChoice,default='Kabadi',null=True)
    username =  models.CharField(max_length=50,null=True)
    class Meta:
        managed = True
        db_table = 'aggregator'

    def __str__(self):
        return self.shop_name + " - "+ self.aggr_category
    
aggrerequesRole =(('aggregator','Aggregator/Collector'),('requestor','Requestor'))
class AggregatorRequestorLogin(models.Model):
    name=models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    password = models.IntegerField(blank=True, null=True)
    role =models.TextField(choices=aggrerequesRole,default='aggregator',null=True)
    
    class Meta:
        managed = True
        db_table = 'aggregator_requestor_login'

    def __str__(self):
        return self.name + "-" +self.role
    
class BuildingDaily(models.Model):
    primary_id = models.CharField(max_length=100)
    parent_id = models.IntegerField()
    dry_waste = models.DecimalField(max_digits=20, decimal_places=5)
    wet_waste = models.DecimalField(max_digits=20, decimal_places=5)
    total_waste = models.DecimalField(max_digits=20, decimal_places=5)
    population = models.IntegerField()
    weight = models.DecimalField(max_digits=20, decimal_places=5)
    date = models.DateField()
    

    class Meta:
        managed = False
        db_table = 'building_daily'
