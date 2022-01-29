import imp
from django.http.response import JsonResponse
from django.forms import model_to_dict

# Create your views here.

import base.queryset as qs
from base.decorators import apiRequest
from modules.eveClient import *
from support.http import jsonFailureResponse, jsonSuccessResponse

from .forms import *
from .models import *


@apiRequest
def industryTable(request, ownerId):
    owner = Character.objects.get(id=ownerId)
    items = IndustryMonitoringItem.objects.filter(owner__id = ownerId)

    materialPrices = TrackingList.get(owner, 'materials').getLastInstance().items_dict
    modulePrices = TrackingList.get(owner, 'items').getLastInstance().items_dict


    res = []
    for item in items:
        bpi = item.blueprint

        newItem = {}
        newItem['id'] = bpi.blueprint.item.id
        newItem['name'] = bpi.blueprint.item.name
        newItem['type'] = bpi.blueprint.item.type
        newItem['materialsCost'] = 0 # Calcular o custo dos materiais requeridos com base em "materialPrices"
        newItem['instalationCost'] = float(item.instalationCost)
        newItem['productionCost'] = newItem['materialsCost'] * (1 + owner.brokersFee) + float(item.instalationCost + item.transportationCost)
        newItem['minSellPrice'] = 0 # productionCost + taxes
        newItem['marketPrice'] = float(modulePrices[bpi.blueprint.item.esiId]['price'])
        newItem['profit'] = newItem['marketPrice'] - newItem['productionCost'] # - taxes
        newItem['quantityInStock'] = item.quantityInStock
        newItem['maxDailyQuantityPerSlot'] = 0 # (pegar da blueprint e calcular o percentual)
        newItem['dailyProfitPerSlot'] = 0
        newItem['dailyBatchCost'] = newItem['productionCost'] * bpi.maxItemsPerDay()
        newItem['profitOverCost'] = newItem['profit'] / newItem['productionCost']

        res.append(newItem)

    return JsonResponse(res, safe = False)


@apiRequest
def createIndustryItem(request, ownerId, stationESIId):
    data = json.loads(request.body)
    existingItems = IndustryMonitoringItem.objects.filter(
        owner__id = ownerId,
        station__esiId = stationESIId,
        name = data['name']
    )
    if existingItems.count() > 0:
        return jsonFailureResponse(error='Object already exists')

    character = Character.objects.get(id = ownerId)
    station = Station.objects.get(esiId = stationESIId)
    item = IndustryMonitoringItem.objects.create(
        owner = character,
        station = station,
        item = Item.objects.get(name = data['name']),
        instalationCost = data['instalationCost'],
        quantityInStock = data['quantityInStock'],
        quantityProducing = data['quantityProducing'],
        estimatedDailyVolume = data['estimatedDailyVolume'],
    )

    return jsonSuccessResponse({'message': 'created'})

'''
@apiRequest
def updateIndustryItem(request, ownerId, itemId):
    item = IndustryMonitoringItem.objects.get(owner__id = ownerId, id = itemId)
    data = json.loads(request.body)
    item.name = data['name']
    res = {
        'data': list(map(lambda item: item.asdict, items))
    }

    return JsonResponse(res)
'''

@apiRequest
def getTrackingList(request, ownerId, name):
    owner = Character.objects.get(id = ownerId)
    trackingList = TrackingList.get(owner, name)
    lastInstance = trackingList.getLastInstance()
    return JsonResponse({
        'data': lastInstance.asdict
    })


@apiRequest
def listItems(request, ownerId):
    items = Item.objects.all()
    return JsonResponse(qs.to_list(items), safe = False)


@apiRequest
def listInputMaterials(request, ownerId):
    owner = Character.objects.get(id=ownerId)
    trackingList = TrackingList.get(owner, 'materials').getLastInstance()
    return JsonResponse(trackingList.items, safe = False)


@apiRequest
def listItemPrices(request, ownerId, itemType):
    owner = Character.objects.get(id=ownerId)
    trackingList = TrackingList.get(owner, itemType).getLastInstance()
    return JsonResponse(trackingList.items, safe = False)