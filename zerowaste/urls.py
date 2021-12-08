from django.urls import path,include
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

# from visits.models import Visits
urlpatterns = [
    path('',views.HomePage, name = 'homepage'),
    # path('garbage_seg/', views.GarbageSeg,name='garbage_seg'),
    path('garbage_seg/', views.WasteSegregationDetailsView,name='garbage_seg'),
    # path('show/',views.show, name='show'),  
    # path('graphs/',views.Graphs, name='graphs'),  
    path('grievance/',views.Grievance, name = 'grievance'),
    path('edit/<int:id>', views.edit),  
    path('update/<int:id>', views.update),  
    path('delete/<int:id>', views.destroy),  
    path('faq/',views.FAQ, name = 'faq'),
    path('feedback/',views.FeedbackView,name ='feedback'),
    path('buildedit/<int:id>',views.Buildedit, name ='buildedit'),
    path('buildupdate/<int:id>',views.Buildupdate, name ='buildupdate'),
    path('buildshow/',views.Buildshow, name='buildshow'),  
    # path('dashboard/',views.Dashboard, name ='dashboard'),
    path('show_wsd/',views.showwastesegregationdetails, name='show_wsd'),
    path('ajax/load_buildings/', views.load_buildings, name='ajax_load_buildings'),
    path('login/', views.user_login, name='login'),
    path("logout", views.logout_request, name="logout"),
    path("register/", views.register_request, name="register"),
    path("emp_detail/",views.emp_detail, name="emp_detail"),
    path("resources/",views.resources, name="resources"),
    # path("showgroup/",views.group,name="showgroup"),
]



# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 