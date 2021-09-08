from django.conf import settings

import math
import multiprocessing as mp

from modules.eveClient import *


def searchItem(itemName):
    foundItems = []
    tranquility = DataSource(ServerNames.TRANQUILITY)
    queryResults, pageCount = tranquility.searchItem(itemName)
    for category, itemIds in queryResults.items():
        workerCount = min(math.ceil(len(itemIds) / 2), settings.MAX_WORKERS)
        #print(f'Using {workerCount} workers') #<<<<<
        with mp.Pool(workerCount) as p:
            foundItems.extend(p.map(tranquility.getItem, itemIds))

    foundItems = list(map(lambda e: e[0], foundItems))

    return foundItems
