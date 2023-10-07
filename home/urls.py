from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views 
from home.views import user_login, user_logout


urlpatterns = [
    path('', views.home, name='home'),
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', user_logout, name='logout'),
    path('tasks/', views.tasks, name='tasks'),
    path('register/', views.register, name='register'),
    path('tasks_by_username/<str:username>/', views.tasks_by_username, name='tasks_by_username'),
    path('update_status/<int:task_id>/', views.update_status, name='update_status'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('graph/', views.graph, name='graph'),
    path('graph2/', views.graph2, name='graph2'),
    # path('graph3/', views.graph3, name='graph3'),
    path('get_tasks/<str:username>/', views.get_tasks, name='get_tasks'),
 
]
