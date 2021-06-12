from decimal import Decimal

def findTopPriceOrder(orders, orderCount, sorted = True):
    if not sorted:
        orders.sort(key = lambda e: e['price'])
    topOrder = None
    actualCount = 0
    for order in orders:
        topOrder = order
        actualCount += order['volume_remain']
        if actualCount >= orderCount:
            break

    return topOrder, actualCount
