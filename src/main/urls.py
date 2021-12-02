from django.urls import path

from .views import *

urlpatterns = [
    path('input-materials/<int:ownerId>', listInputMaterials, name='input_materials_list'),
    path('input-materials/<int:ownerId>/update', updateInputMaterialsPrices, name='input_materials_update'),
    path('items/price/<int:ownerId>', listItemPrices, name='item_price_list'),
    path('items/price/<int:ownerId>/update', updateItemPrices, name='item_price_update'),
]
