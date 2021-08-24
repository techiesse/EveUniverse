from django.shortcuts import render

# Create your views here.
from .models import *

def listBlueprints(request):
    blueprints = Blueprint.objects.all()
    context = {
        'blueprints': blueprints,
    }

    return render(request, 'EveAssets/blueprint_list.html', context)


def createBlueprint(request):
    pass
