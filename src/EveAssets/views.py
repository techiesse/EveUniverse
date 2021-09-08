from django.conf import settings
from django.shortcuts import render

# Create your views here.
import multiprocessing as mp
import re

from modules.eveClient import *

from EveAssets import domain
from .forms import *
from .models import *

def listBlueprints(request):
    blueprints = Blueprint.objects.all()
    context = {
        'blueprints': blueprints,
    }

    return render(request, 'EveAssets/blueprint_list.html', context)


def createBlueprint(request, ):
    foundItems, form = handleBlueprintSearch(request)
    bp = Blueprint.objects.create()

    context = {
        'form': form,
        'results': foundItems,
    }

    return render(request, 'EveAssets/blueprint_create.html', context)


def searchBlueprint(request):
    foundItems, form = handleBlueprintSearch(request)
    if foundItems != []:
        return redirect('blueprint_list')

    context = {
        'form': form,
        'results': foundItems,
    }

    return render(request, 'EveAssets/blueprint_create.html', context)


def handleBlueprintSearch(request):
    form = BlueprintSearchForm(request.POST or None)
    foundItems = []
    if form.is_valid():
        searchTerm = form.cleaned_data['searchTerm']
        m = re.search('blueprint', searchTerm, re.IGNORECASE)
        if m is None:
            searchTerm += ' blueprint'

        foundItems = domain.searchItem(searchTerm)

    return foundItems, form


def searchItem(request):
    form = ItemSearchForm(request.POST or None)
    foundItems = []
    if form.is_valid():
        itemName = form.cleaned_data['itemName']
        foundItems = domain.searchItem(itemName)

    context = {
        'form': form,
        'results': foundItems,
    }

    return render(request, 'EveAssets/search.html', context)
