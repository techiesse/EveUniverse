from django.db import models

from contextlib import suppress

import json
import math

# Create your models here.
import base.queryset as qs

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
    runCycleTime = models.IntegerField() # Seconds to complete 1 run.
    maxProductionLimit = models.IntegerField()

    def __str__(self):
        return self.name

    def filterComponents(self, *q, **query):
        return self.blueprintcomponent_set.filter(*q, **query)

    @property
    def components(self):
        return qs.tolist(self.filterComponents)


class BlueprintComponent(models.Model):
    blueprint = models.ForeignKey(Blueprint, on_delete=models.CASCADE, related_name='components')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    models.UniqueConstraint(fields = ['blueprint', 'item'], name='unique_blueprint_component')

    @property
    def name(self):
        return self.item.name

    def __str__(self):
        return self.name


class BlueprintInstance(models.Model):
    '''A Blueprint suitable for production. Can potencially be researched'''
    blueprint = models.ForeignKey(Blueprint, on_delete=models.CASCADE)
    materialEfficiency = models.IntegerField(default=0)
    timeEfficiency = models.IntegerField(default=0)

    def calcRequiredMaterials(self, runCount):
        ret = {'runCount': runCount}
        for item in self.blueprint.components.all():
            ret[item.id] = {
                'item': item,
                'quantity': effectiveMaterialQuantity(item.quantity, self.me, runCount),
            }
        return ret

    def __str__(self):
        return f'{self.blueprint.name} ({self.materialEfficiency}/{self.timeEfficiency})'

    @property
    def me(self):
        '''Material efficiency as a ratio instead of a percentage'''
        return self.materialEfficiency / 100

    @me.setter
    def me(self, value):
        self.materialEfficiency = round(value * 100)

    @property
    def te(self):
        '''Time efficiency as a ratio instead of a percentage'''
        return self.timeEfficiency / 100

    @te.setter
    def te(self, value):
        self.timeEfficiency = round(value * 100)

    @property
    def producedItem(self):
        return self.blueprint.item

    @property
    def components(self):
        return self.blueprint.components

    def fixTime(self, time, industryLevel = 0, advancedIndustryLevel = 0):
        '''Calculates the real time necessary to build an item considering time efficiency and player skills.

        Time reductions are calculated per group, meaning BP time efficiency is one group, industry skill is another
        group and advanced industry skill another one.

        The increase in the percentage is linear within one group. For example, if the player has level 3 industry, the
        discount related to that skill will be 3 * 0.04 = 0.12.

        The discount of each group is applied on top of each other, which leads to the expression:

        realTime = baseTime * (1 - TE) * (1 - IndustryLevel * 0.04) * (1 - AdvancedIndustryLevel * 0.03)
        '''
        return time * (1 - self.te) * (1 - industryLevel * 0.04) * (1 - advancedIndustryLevel * 0.03)

    def maxItemsPerDay(self, industryLevel = 0, advancedIndustryLevel = 0):
        ''' Calculates the maximum amount of items that can be produced in 24h with current BP and skills

        maxItemsPerDay = itemsPerCycle * cyclesPerDay
        maxItemsPerDay = itemsPerCycle * (secondsPerDay / cycleTime)
        '''
        cyclesPerDay = (24 * 3600) / self.fixTime(self.blueprint.runCycleTime, industryLevel, advancedIndustryLevel)
        return math.floor( self.blueprint.runOutputCount * cyclesPerDay)


def effectiveMaterialQuantity(quantity, materialEfficiency, runCount):
    return math.ceil(runCount * quantity * (1 - materialEfficiency))