from django.contrib import admin
from .models import EmployeeDetails
# Register your models here.
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ( 'username', 'first_name','email',)
    list_filter = ( 'username', 'first_name', 'email','Ward','prabhag')
    # ordering = ('-start_date',)
    list_display = ( 'username', 'first_name','email','Ward','prabhag')
    fieldsets = (
        (None, {'fields': ( 'username', 'first_name','email','Ward','prabhag')}),
        
        
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'username', 'first_name','email','password1', 'password2', 'Ward','prabhag')}
         ),
    )


admin.site.register(User, UserAdminConfig)
admin.site.register(EmployeeDetails)
