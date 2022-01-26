import imp
from django.http.response import JsonResponse
from django.forms import model_to_dict

# Create your views here.

from base.decorators import apiRequest
from modules.eveClient import *
from support.http import jsonFailureResponse, jsonSuccessResponse

from .forms import *
from .models import *


@apiRequest
def industryTable(request, ownerId):
    items = IndustryMonitoringItem.objects.filter(owner__id = ownerId)
    res = {
        'data': list(map(lambda item: item.asdict, items))
    }

    return JsonResponse(res)


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


@apiRequest
def updateIndustryItem(request, ownerId, itemId):
    item = IndustryMonitoringItem.objects.get(owner__id = ownerId, id = itemId)
    data = json.loads(request.body)
    item.name = data['name']
    res = {
        'data': list(map(lambda item: item.asdict, items))
    }

    return JsonResponse(res)


@apiRequest
def getTrackingList(request, ownerId, name):
    trackingList = TrackingList.objects.get(name = name)
    lastInstance = trackingList.getLastInstance()
    return JsonResponse({
        'data': lastInstance.asdict
    })

@apiRequest
def listItems(request, ownerId):
    items = Item.objects.all()

    return JsonResponse(list(map(model_to_dict, items)), safe = False)