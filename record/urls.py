from django.urls import path
from .views import get_list_of_records, download_record

app_name = 'record'

urlpatterns = [
    path('list/<uuid:cam_uuid>/', get_list_of_records, name='get_records_list'),
    path('download/<uuid:cam_uuid>/<str:filename>', download_record, name='download_record'),
]
