from django.urls import path,include,re_path
from . import views
from .views import document_list, static_files_view
from django.conf import settings
from django.conf.urls.static import static

# from visits.models import Visits
urlpatterns = [
    path('',views.HomePage, name = 'homepage'),
    # path('',views.restrictedHomePage,name = 'restrictedHomePage'),
    path('dashboard/',views.base, name = 'dashboard'),
    # path('garbage_seg/', views.GarbageSeg,name='garbage_seg'),
    path('garbage_seg/', views.WasteSegregationDetailsView,name='garbage_seg'),
    # path('show/',views.show, name='show'),  
    # path('graphs/',views.Graphs, name='graphs'),  
    path('grievance/',views.Grievance, name = 'grievance'),
    path('table/<str:id>',views.table, name = 'table'),
    path('edit/<int:id>', views.edit),  
    path('update/<int:id>', views.update),  
    path('delete/<int:id>', views.destroy),  
    path('faq/',views.FAQ, name = 'faq'),
    path('feedback/',views.FeedbackView,name ='feedback'),
    path('buildedit/<str:id>',views.Buildedit, name ='buildedit'),
    path('buildupdate/<str:id>',views.Buildupdate, name ='buildupdate'),
    path('buildshow/',views.Buildshow, name='buildshow'),  
    path('road_buffer/',views.road_bufferView, name ='road_buffer'),
    path('show_wsd/',views.showwastesegregationdetails, name='show_wsd'),
    path('ajax/load_buildings/', views.load_buildings, name='ajax_load_buildings'),
    path('login/', views.user_login, name='login'),
    path("logout", views.logout_request, name="logout"),
    path("reset_pass",views.reset_pass, name='reset_pass'),
    # path("change_pass",views.change_pass, name='change_reset'),
    # path("password_change_done",views.password_change_done, name='password_change_done'),
    # path("password_reset_done",views.password_reset_done, name='password_reset_done'),
    # path("password_reset_confirm",views.password_reset_confirm, name='password_reset_confirm'),
    # path("password_reset_complete",views.password_reset_complete, name='password_reset_complete'),
    path("register/", views.register_request, name="register"),
    path("emp_detail/",views.emp_detail, name="emp_detail"),
    path("hrd_detail/",views.hrd_detail, name="hrd_detail"),
    path('ajax/load-prabhag/', views.load_prabhag, name='ajax_load_prabhag'),
    path("resources/",views.resources, name="resources"),
    path("resources_orig/",views.resources_orig, name="resources_orig"),
    path("video/",views.static_files_view, name="video"),
    
    # path("showgroup/",views.group,name="showgroup"),
    path("w61wcd/",views.w61wcd, name="w61wcd"),
    path('dashboard_piecharts/',views.Piecharts, name="dashboard_piecharts"),
    path('dashboard2/',views.dashboard2, name="dashboard2"),
    path('dashboard2_1/',views.dashboard2_1, name="dashboard2_1"),
    path('dashboard2_2/',views.dashboard2_2, name="dashboard2_2"),
   
    # path('tree_census_charts/',views.tree_census_charts, name="tree_census_charts"),
    path('garbage_seg_rev/', views.WasteSegregationDetailsRevisedView,name='garbage_seg_rev'),
    path('compost_form/', views.compost_form,name='compost_form'),
    # path('documents/<int:document_id>/<path:document_filename>/', custom_serve, name='wagtaildocs_serve'),
    path('student_registration/',views.student_registration, name='student_registration'),
    path('document-list/', document_list, name='document_list'),
    path('static_files_view/', static_files_view, name='static_files_view'),
    path('document_list/', document_list, name='document_list'),

    re_path(r'^list_articles/', views.list_articles, name='list_articles'),
    path('plr_map',views.plr_map, name='plr_map'),
    path('plr_report',views.plr_report, name='plr_report'),
]



# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 