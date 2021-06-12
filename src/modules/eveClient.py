import json
import requests

MARKET_BASE_URL = 'https://esi.evetech.net'

class ServerNames:
    TRANQUILITY = 'tranquility'
    SINGULARITY = 'singularity'


CATEGORIES = {
    'AGENT': 'agent',
    'ALLIANCE': 'alliance',
    'CHARACTER': 'character',
    'CONSTELLATION': 'constellation',
    'CORPORATION': 'corporation',
    'FACTION': 'faction',
    'INVENTORY_TYPE': 'inventory_type',
    'REGION': 'region',
    'SOLAR_SYSTEM': 'solar_system',
    'STATION': 'station',
}


class DataSource:
    def __init__(self, serverName):
        self.serverName = serverName

    def request(self, resource, **filters):
        filters['datasource'] = self.serverName
        filterStr = '&'.join([f'{k}={v}' for k, v in filters.items()])
        url = f'{MARKET_BASE_URL}/{resource}?{filterStr}'

        response = requests.get(url)
        response.raise_for_status()

        jsonResponse = response.content
        pageCount = int(response.headers.get('X-Pages') or 1)
        return json.loads(jsonResponse), pageCount

    def getSystem(self, systemId):
        return self.request(f'latest/universe/systems/{systemId}')

    def getSystems(self):
        return self.request(f'latest/universe/systems/')

    def getConstelation(self, constellationId):
        return self.request(f'latest/universe/constellations/{constellationId}')

    def getItem(self, itemId):
        res = self.request(f'latest/universe/types/{itemId}')
        return res

    def getItemName(self, itemId):
        #https://esi.evetech.net/v3/universe/types/2048?datasource=tranquility&type_id=2048
        item = self.getItem(itemId)
        return item['name']

    def search(self, term, categories, strict=False):
        path = 'latest/search'
        categories_param = ",".join(categories)
        #print(categories_param)
        return self.request(path, search = term, categories = categories_param, strict = strict)


    def searchItem(self, itemName, strict=False):
        return self.search(itemName, ['inventory_type'], strict=strict)


    def getMarketOrders(self, regionId, solarSystemId = None, itemId = None, orderType = 'all'):
        path = f'latest/markets/{regionId}/orders'

        params = {
            'order_type': orderType,
        }
        if itemId is not None:
            params['type_id'] = itemId

        orders = []
        currentOrders = None
        currentPage = 1
        while currentOrders != []:
            currentOrders, pageCount = self.request(path, page = currentPage, **params)
            filteredOrders = currentOrders
            if solarSystemId is not None:
                filteredOrders = list(filter(lambda o: int(o['system_id']) == int(solarSystemId), currentOrders))
            orders.extend(filteredOrders)

            if currentPage >= pageCount:
                break
            currentPage += 1

        return orders


#https://esi.evetech.net/v1/markets/10000001/orders/?datasource=tranquility&order_type=sell&page=1
#https://esi.evetech.net/v3/universe/types/2048?datasource=tranquility&type_id=2048

if __name__ == '__main__':
    print(Categories.all())
