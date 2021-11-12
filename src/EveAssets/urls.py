from django.urls import path

from .views import *

urlpatterns = [
    path('blueprint/create/', createBlueprint, name='blueprint_create'),
    path('blueprint/list/', listBlueprints, name='blueprint_list'),
    path('blueprint/search/', searchBlueprint, name='blueprint_search'),
    path('search', searchItem, name='item_search'),
]
