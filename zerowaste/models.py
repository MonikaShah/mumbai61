# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from map.models import *
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
class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(max_length=150, unique=True)
    # first_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(null=True,blank=True)
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
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


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
    grievance = models.TextField(blank=False, null=False, default='Testing')
    # grievance = models.TextField(null=True, default=None, blank=True),
    uploaded_at = models.DateTimeField(auto_now_add=True)
    grievance_no = models.CharField(max_length=100,null=True, default=None, blank=True)

    class Meta:
        managed = True
        db_table = 'grievance'

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

# class OsmBuildings29Oct21(models.Model):
#     geom = models.TextField(blank=True, null=True)  # This field type is a guess.
#     fid = models.IntegerField(blank=False, null=False)
#     osm_id = models.IntegerField(blank=True, null=True)
#     addrstreet = models.CharField(max_length=200, blank=True, null=True)
#     building = models.CharField(max_length=80, blank=True, null=True,default = "TestBuilding")
#     name = models.CharField(max_length=80, blank=True, null=True, default = "TestName")
#     num_flats = models.IntegerField(blank=True, null=True, default =1)
#     wings = models.IntegerField(blank=True, null=True,default=1)
#     region = models.CharField(max_length=50, blank=True, null=True,default = "TestRegion")

#     class Meta:
#         managed = False
#         db_table = 'osm_buildings_29oct21'

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
    adminward =models.CharField(max_length=50,default = 'Ward-KWest')
    councillorward = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    emp_category =models.CharField(max_length = 100)
    emp_name =models.CharField(max_length = 100)
    emp_mobile =models.IntegerField()

    class Meta:
        managed = True
        db_table = 'employee_details'

    def __str__(self):
        return self.emp_name