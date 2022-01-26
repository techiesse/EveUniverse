from django.urls import path

from .api import *
from .views import *

urlpatterns = [
    path('input-materials/<int:ownerId>/', listInputMaterials, name='input_materials_list'),
    path('input-materials/<int:ownerId>/update/', updateInputMaterialsPrices, name='input_materials_update'),

    path('items/price/<int:ownerId>/', listItemPrices, name='item_price_list'),
    path('items/price/<int:ownerId>/update/', updateItemPrices, name='item_price_update'),

    path('api/items/<int:ownerId>/list/', listItems, name = 'item_list'),
    path('api/industry/monitoring/<int:ownerId>/', industryTable, name='industry_monitoring'),
    path('api/tracking-list/<int:ownerId>/<str:name>/', getTrackingList, name='tracking_list'),
]
