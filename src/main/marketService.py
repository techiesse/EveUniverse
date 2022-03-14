

def calcMinSellPrice(acquisitionCost, salesTax, brokersFee):
    '''Calculates the price required for selling without losing money
    The acquisition cost can be the value at which the item has been purchased or the production cost (both including taxes)

    Calculation:
    profit = sellPrice - acquisitionCost - salesTaxCost - brokersFeeCost
    profit = sellPrice - acquisitionCost - sellPrice * salesTax - sellPrice * brokersFee
    profit = sellPrice - acquisitionCost - sellPrice * (salesTax + brokersFee)
    profit = sellPrice * (1 - (salesTax + brokersFee)) - acquisitionCost

    Making the profit 0 we find the desired value:
    0 = minSellPrice * (1 - (salesTax + brokersFee)) - acquisitionCost
    minSellPrice * (1 - (salesTax + brokersFee)) =  acquisitionCost
    minSellPrice = acquisitionCost / (1 - (salesTax + brokersFee))
    '''

    return acquisitionCost / (1 - (salesTax + brokersFee))


def calcProfit(marketPrice, acquisitionCost, salesTax, brokersFee):
    '''Calculates the profit selling for the current market price using a sell order'''
    return marketPrice * (1 - salesTax - brokersFee) - acquisitionCost
