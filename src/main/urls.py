from django.urls import path

from main import api
from .views import *

urlpatterns = [
    # Industry
    path('input-materials/<int:ownerId>/', listInputMaterials, name='input_materials_list'),
    path('input-materials/<int:ownerId>/update/', updateInputMaterialsPrices, name='input_materials_update'),

    path('items/price/<int:ownerId>/', listItemPrices, name='item_price_list'),
    path('items/price/<int:ownerId>/update/', updateItemPrices, name='item_price_update'),

    # API:
    path('api/items/<int:ownerId>/list/', api.listItems, name = 'item_list'),
    path('api/industry/monitoring/<int:ownerId>/', api.industryTable, name='industry_monitoring'),
    path('api/tracking-list/<int:ownerId>/<str:name>/', api.getTrackingList, name='tracking_list'),

    path('api/input-materials/<int:ownerId>/', api.listInputMaterials, name='api-input_materials_list'),

    path('api/item-prices/<int:ownerId>/<itemType>/', api.listItemPrices, name='api-item_price_list'),
    path('api/item-prices/<int:ownerId>/<itemType>/update/', api.updateItemPrices, name='api-item_prices_update'),

]
