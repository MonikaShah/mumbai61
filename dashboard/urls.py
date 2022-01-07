from django.urls import path
from dashboard.views import Dash

urlpatterns = [
    path('prabhag61/',Dash.as_view(), name = 'dash'),
]

