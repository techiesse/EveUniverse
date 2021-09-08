from django.shortcuts import render, redirect

# Create your views here.

from .forms import *
from .models import *
from modules.eveClient import *

def home(request):
    return render(request, 'main/home.html')


def listInputMaterials(request, ownerId):
    trackingLists = TrackingList.objects.filter(template__name='materials', template__owner__id=ownerId).order_by('-created_at')
    owner = Character.objects.get(id=ownerId)

    trackingList = trackingLists[0]
    items = trackingList.trackeditem_set.all()
    context = {
        'items': items,
        'owner': owner,
    }
    return render(request, 'main/input-materials.html', context)


def listItemPrices(request, ownerId):
    trackingLists = TrackingList.objects.filter(template__name='items', template__owner__id=ownerId).order_by('-created_at')
    owner = Character.objects.get(id=ownerId)

    trackingList = trackingLists[0]
    items = trackingList.trackeditem_set.all()
    context = {
        'items': items,
        'owner': owner,
    }
    return render(request, 'main/item-price.html', context)


def updateInputMaterials(request, ownerId):
    trackingList = TrackingListTemplate.objects.get(name='materials', owner__id=ownerId)
    trackingList.generateEstimate()

    return redirect('input_materials_list', ownerId)


def updateItemPrices(request, ownerId):
    trackingList = TrackingListTemplate.objects.get(name='items', owner__id=ownerId)
    trackingList.generateEstimate()

    return redirect('item_price_list', ownerId)
