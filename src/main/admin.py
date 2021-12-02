from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Character)
admin.site.register(TrackingList)
admin.site.register(TrackedItem)
admin.site.register(TrackingListInstance)
admin.site.register(TrackedItemInstance)
