from django.urls import path

from .views import *

urlpatterns = [
    path('blueprint/list/', listBlueprints, name='blueprint_list'),
    path('blueprint/create/', createBlueprint, name='blueprint_create'),
]
