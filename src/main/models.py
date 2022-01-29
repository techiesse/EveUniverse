from contextlib import suppress
from decimal import Decimal
from django.db import models

import najha.functional as f

from modules import eveClient, eveStatic
from modules.utils import *

from base.models import *
from EveAssets.models import *

from .domain import market

# Create your models here.
'''
class Config:
    key = models.CharField(max_length=255, unique=True)
    value = models.Text()
    value_type = models.CharField(max_length=20, default='string'
        choices = [
            ('int', 'int'),
            ('float', 'float'),
            ('string', 'string'),
            ('boolean', 'boolean'),
        ]
    )
'''

class Character(models.Model):
    name = models.CharField(max_length=255, unique = True)
    salesTax = models.FloatField()
    brokersFee = models.FloatField()

    def __str__(self):
        return f'{self.name} (ST={self.salesTax:.3}, BF={self.brokersFee:.3})'


# Inventory App
class Inventory(models.Model):
    owner = models.OneToOneField(Character, on_delete=models.CASCADE)


class InventoryItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='items')

    @property
    def name(self):
        return self.item.name


# Market:
class TrackingList(models.Model):
    owner = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    orderCount = models.IntegerField()

    models.UniqueConstraint(fields = ['owner', 'name'], name='unique_tracking_list')

    def __str__(self):
        return self.name

    def addItem(self, name):
        item = TrackedItem.objects.create(
            item = Item.objects.get(name = name),
            trackingList = self,
        )

    def generateEstimate(self):
        priceList = TrackingListInstance.fromTemplate(self)

        region = priceList.station.solarSystem.region

        # Obter preços dos materiais:
        tranquility = eveClient.DataSource(eveClient.ServerNames.TRANQUILITY)
        optionalParams = {}
        items = self.items.all().order_by('item__name')
        for item in items:
            orders = tranquility.getMarketOrders(region.esiId, itemId = item.item.esiId, orderType = 'sell', **optionalParams)
            orders = f.map(lambda o: {
                'price': o['price'],
                'volume_remain': o['volume_remain'],
                }, orders
            )
            orders.sort(key = lambda o: o['price'])

            topOrder, actualCount = market.findTopPriceOrder(orders, self.orderCount)
            price = None
            note = None
            if topOrder is None:
                note = 'No order found'
            else:
                if actualCount < self.orderCount:
                    note = f'Only {actualCount} orders found'
                price = Decimal(topOrder['price'])

            priceList.createItem(item, price, note)

        return priceList


    def getLastInstance(self):
        instance = None
        with suppress(TrackingListInstance.DoesNotExist):
            instance = self.trackinglistinstance_set.latest('id')

        return instance

    @classmethod
    def get(cls, owner, name):
        return cls.objects.get(owner = owner, name = name)


class TrackedItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    trackingList = models.ForeignKey(TrackingList, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return self.item.name


class TrackingListInstance(Entity):
    template = models.ForeignKey(TrackingList, null=True, on_delete=models.SET_NULL)
    orderCount = models.IntegerField()

    def __str__(self):
        return f'{self.template.name} ({self.id})'

    @property
    def owner(self):
        return self.template.owner

    @property
    def station(self):
        return self.template.station

    @classmethod
    def fromTemplate(cls, template):
        return cls.objects.create(
            template = template,
            orderCount = template.orderCount,
        )

    def createItem(self, item, price, note):
        return TrackedItemInstance.objects.create(
            item = item.item,
            trackingList = self,
            price = price,
            note = note,
        )

    @property
    def items(self):
        return list(map(lambda item: item.asdict, self.trackediteminstance_set.all()))

    @property
    def items_dict(self):
        return {item.item.esiId: item.asdict for item in self.trackediteminstance_set.all()}

    @property
    def asdict(self):
        return {
            'name': self.template.name,
            'orderCount': self.orderCount,
            'items': self.items,
        }

    @classmethod
    def ownedBy(cls, owner):
        return cls.objects.filter(template__owner = owner)


class TrackedItemInstance(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    trackingList = models.ForeignKey(TrackingListInstance, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.item.name} {self.price:.2f} ISK'

    @classmethod
    def fromTemplate(cls, itemTemplate, price):
        return cls.objects.create(
            item = itemTemplate.item,
            trackingList = itemTemplate.trackingList,
            note = itemTemplate.note,
            price = price,
        )

    @property
    def asdict(self):
        res = self.item.asdict
        res.update({
            'price': self.price,
            'note': self.note,
        })
        return res


# Industry
class IndustryMonitoringItem(models.Model):
    owner = models.ForeignKey(Character, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)

    models.UniqueConstraint(fields = ['owner', 'station'], name='unique_monitoring_item')

    blueprint = models.ForeignKey(BlueprintInstance, on_delete=models.CASCADE)
    instalationCost = models.DecimalField(max_digits=30, decimal_places=2)
    transportationCost = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    quantityInStock = models.IntegerField(default=0)
    quantityProducing = models.IntegerField(default=0)
    estimatedDailyVolume = models.IntegerField()

    @property
    def name(self):
        return self.item.name

    @property
    def type(self):
        return self.item.type

    def calcProductionCost(self):
        pass

    def minSellPrice(self):
        pass

    def profit(self):
        pass

    def maxDailyProfitPerSlot(self):
        pass

    @property
    def asdict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'station': self.station.id,
            'item': self.item.asdict,
            'instalationCost': float(self.instalationCost),
            'productionCost': self.calcProductionCost(),
            'quantityInStock': self.quantityInStock,
            'quantityProducing': self.quantityProducing,
            'estimatedDailyVolume': self.estimatedDailyVolume,
        }
