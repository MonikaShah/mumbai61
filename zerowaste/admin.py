from django.contrib import admin
from .models import EmployeeDetails,HumanResourceData
# Register your models here.
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ( 'username', 'email',)
    list_filter = ( 'username',  'email','designation','role','area','Ward','prabhag','is_active', 'is_staff')
    # ordering = ('-start_date',)
    list_display = ( 'username', 'email','designation','role','area','Ward','prabhag','is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ( 'username', 'email','role','designation','area','Ward','prabhag')}),
        ('Group Permissions', {
    'fields': ('groups', 'user_permissions', )
}),
         ('Permissions', {'fields': ('is_staff', 'is_active')}),
        
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'username', 'email','password1', 'password2','designation','role','area', 'Ward','prabhag')}
         ),
    )


admin.site.register(User, UserAdminConfig)
admin.site.register(EmployeeDetails)
admin.site.register(HumanResourceData)
