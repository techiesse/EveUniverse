from django.conf import settings

def loadSolarSystems():
    solarSystems = loadJson(os.path.join(settings.BASE_DIR, 'resources', 'systems.json'))
    return solarSystems
