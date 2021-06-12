from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Character)
admin.site.register(TrackingListTemplate)
admin.site.register(TrackedItemTemplate)
admin.site.register(TrackingList)
admin.site.register(TrackedItem)
