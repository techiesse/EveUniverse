from django.http.response import JsonResponse
from django.forms import model_to_dict

# Create your views here.

import base.queryset as qs
from base.decorators import apiRequest
from modules.eveClient import *
from support.http import jsonFailureResponse, jsonSuccessResponse

from .forms import *
from .models import *

from .marketService import calcMinSellPrice, calcProfit
from .industryService import calcProductionCost


def calcMaxItemsPerDay(bpi, owner):
    industryLevel = owner.characterskill_set.get(skill__name = 'Industry').level
    advancedIndustryLevel = owner.characterskill_set.get(skill__name = 'Advanced Industry').level

    return bpi.maxItemsPerDay(industryLevel, advancedIndustryLevel)


@apiRequest
def industryTable(request, ownerId):
    owner = Character.objects.get(id=ownerId)
    items = IndustryMonitoringItem.objects.filter(owner__id = ownerId)

    materialPriceList = TrackingList.get(owner, 'materials').getLastInstance()
    if materialPriceList is None:
        return jsonFailureResponse('Material price list is empty. Did you forget to update the list?')

    modulePriceList = TrackingList.get(owner, 'items').getLastInstance()
    if modulePriceList is None:
        return jsonFailureResponse('Module price list is empty. Did you forget to update the list?')

    materialPrices = materialPriceList.itemsDict
    modulePrices = modulePriceList.itemsDict

    res = []
    for item in items:
        bpi = item.blueprint

        newItem = {}
        newItem['id'] = bpi.blueprint.item.id
        newItem['name'] = bpi.blueprint.item.name
        newItem['type'] = bpi.blueprint.item.type
        newItem['materialsCost'] = item.calcMaterialsCost(materialPrices) # Calcular o custo dos materiais requeridos com base em "materialPrices"
        newItem['instalationCost'] = item.unitInstalationCost
        newItem['productionCost'] = calcProductionCost(newItem['materialsCost'], item.unitInstalationCost, item.transportationCost)
        newItem['minSellPrice'] = calcMinSellPrice(newItem['productionCost'], owner.salesTax, owner.brokersFee)
        newItem['marketPrice'] = float(modulePrices[bpi.blueprint.item.esiId]['price'])
        newItem['profit'] = calcProfit(newItem['marketPrice'], newItem['productionCost'], owner.salesTax, owner.brokersFee)
        newItem['quantityInStock'] = item.quantityInStock
        newItem['maxDailyQuantityPerSlot'] = calcMaxItemsPerDay(bpi, owner)
        #newItem['dailyProfitPerSlot'] = 0
        newItem['potentialDailyProfit'] = newItem['profit'] * item.estimatedDailyVolume / 10
        newItem['dailyBatchCost'] = newItem['productionCost'] * newItem['maxDailyQuantityPerSlot']
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
        'data': lastInstance.asdict if lastInstance is not None else {}
    })


@apiRequest
def listItems(request, ownerId):
    items = Item.objects.all()
    return JsonResponse(qs.to_list(items), safe = False)


@apiRequest
def listInputMaterials(request, ownerId):
    return listItemPrices(request, ownerId, 'materials')


@apiRequest
def listItemPrices(request, ownerId, itemType):
    owner = Character.objects.get(id=ownerId)
    trackingList = TrackingList.get(owner, itemType).getLastInstance()
    items = trackingList.items if trackingList is not None else []
    return JsonResponse(items, safe = False)


@apiRequest
def updateItemPrices(request, ownerId, itemType):
    owner = Character.objects.get(id=ownerId)
    trackingList = TrackingList.get(owner, itemType)
    trackingList.generateEstimate()

    return JsonResponse({'success': True})