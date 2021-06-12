import json

def loadJson(sourceFile):
    with open(sourceFile) as source:
        result = json.load(source)

    return result


def getRegionById(regions, id):
    res = None
    for k, region in regions.items():
        if region['id'] == id:
            res = region
            break
    return res


def splitN(n, text):
    i = 0
    parts = []
    N = len(text)
    while i < N:
        parts.append(text[i:i+n])
        i += n
    return parts


def reverseStr(text):
    return text[::-1]
