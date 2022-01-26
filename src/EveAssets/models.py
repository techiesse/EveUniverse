from django.db import models

from contextlib import suppress

import json
import math

# Create your models here.
from base.predicates import raises

class ESI_Entity(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=255, unique = True)
    esiId = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class Item(ESI_Entity):
    type = models.CharField(max_length = 255,
        null = True, blank = True,
        choices=[
            ('component', 'Component'),
            ('mineral', 'Mineral'),
            ('module', 'Module'),
            ('rig', 'Rig'),
            ('salvage', 'Salvage'),
        ]
    )

    @classmethod
    def loadJson(cls, path):
        with open(path) as source:
            jsonData = json.load(source)

        for item in jsonData:
            cls.objects.create(
                name = item['name'],
                esiId = item['id'],
                type = item['type'],
            )

    def hasBlueprint(self):
        return not raises(Exception, lambda: self.blueprint)

    @property
    def asdict(self):
        return {
            'name': self.name,
            'esiId': self.esiId,
            'type': self.type,
        }


class Region(ESI_Entity):
    @classmethod
    def loadJson(cls, path):
        with open(path) as source:
            jsonData = json.load(source)

        for name, data in jsonData.items():
            cls.objects.create(
                name = name,
                esiId = data['id'],
            )


class SolarSystem(ESI_Entity):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    @classmethod
    def loadJson(cls, path):
        with open(path) as source:
            jsonData = json.load(source)

        for name, data in jsonData.items():
            cls.objects.create(
                name = name,
                esiId = data['id'],
                region = Region.objects.get(name=data['region'])
            )


class Station(ESI_Entity):
    solarSystem = models.ForeignKey(SolarSystem, on_delete=models.CASCADE)

    @classmethod
    def loadJson(cls, path):
        with open(path) as source:
            jsonData = json.load(source)

        for alias, item in jsonData.items():
            cls.objects.create(
                name = item['name'],
                esiId = item['id'],
                solarSystem = SolarSystem.objects.get(name=item['system']),
            )


# For now I'm not dealing with research, copying and invention
class Blueprint(ESI_Entity):
    '''Base Blueprint. Not considering the effects of research or copy'''
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    runOutputCount = models.IntegerField(default = 1) # Number of items produced per run.
    runCicleTime = models.IntegerField() # Seconds to complete 1 run.
    maxProductionLimit = models.IntegerField()


class BlueprintComponent(models.Model):
    blueprint = models.ForeignKey(Blueprint, on_delete=models.CASCADE, related_name='components')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    unique_together = ['blueprint', 'item']

    @property
    def name(self):
        return self.item.name


class BlueprintInstance(models.Model):
    '''A Blueprint suitable for production. Can potencially be researched'''
    blueprint = models.ForeignKey(Blueprint, on_delete=models.CASCADE)
    materialEfficiency = models.IntegerField(default=0)
    timeEfficiency = models.IntegerField(default=0)

    def calc_required_materials(self, runCount):
        ret = {'runCount': runCount}
        for item in self.blueprint.components.all():
            ret[item.id] = {
                'item': item,
                'quantity': math.floor(runCount * item.quantity * (1 + self.materialEfficiency / 100)),
            }
        return ret

    @property
    def me(self):
        return self.materialEfficiency

    @me.setter
    def me(self, value):
        self.materialEfficiency = value

    @property
    def te(self):
        return self.timeEfficiency

    @te.setter
    def te(self, value):
        self.timeEfficiency = value
