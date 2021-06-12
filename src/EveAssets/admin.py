from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Region)
admin.site.register(SolarSystem)
admin.site.register(Station)
admin.site.register(Blueprint)
admin.site.register(BlueprintComponent)
admin.site.register(BlueprintInstance)
