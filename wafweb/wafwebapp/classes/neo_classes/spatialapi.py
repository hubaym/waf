import requests
import classes.constant.wafconnection as wcon
from neoquery import NeoQuery
import json
from classes.constant.waflog import WafLog

WS_URL = wcon.NEO_HOST +'/db/data/'

class SpatialApi():
    
    def __init__(self):
        self.__url = WS_URL

    def getLayer(self, name):
        
        extraURL = 'ext/SpatialPlugin/graphdb/getLayer'
        
        json = dict()
        json['layer'] = name
        
        WafLog().neologger.info(self.POST(self.__url + extraURL, json))

    def addPointLayer(self, name):
        
        extraURL = 'ext/SpatialPlugin/graphdb/addSimplePointLayer'
        
        json = dict()
        json['layer'] = name
        json['lat'] = 'lat'
        json['lon'] = 'lan'
        
        self.POST(self.__url + extraURL, json)
        
    def addSpatialIndex(self, name):
        
        extraURL = 'index/node/'
       
        json = dict()
        json['name'] = name
        json['config'] = {
                     "provider" : "spatial",
                     "geometry_type" : "point",
        "lat" : "lat",
        "lon" : "lan"
                    }
        
        WafLog().neologger.info(json)
        
        self.POST(self.__url + extraURL, json)
        
        
    def addNodeToIndex(self, name, id):
        extraURL = 'ext/SpatialPlugin/graphdb/addNodeToLayer'
        json = dict()
        json['layer'] = name
        json['node'] = self.__url  + 'node/' + str(id)
        
        
        self.POST(self.__url + extraURL, json)
        
    def addAllNodeToIndex(self, name):
        WafLog().neologger.info('addAllNodeToIndex started')
        neoq = NeoQuery()
        i=0
        for id in neoq.getAllCityID():
            self.addNodeToIndex(name,id[0])
            i+=1
            if i%1000==0:
                WafLog().neologger.info('addAllNodeToIndex process {0}'.format(i))
            
            
        WafLog().neologger.info('addAllNodeToIndex finished')
        
            
    def findGeometriesWithinDistance(self, layer, x, y, dist):
        
        extraURL = 'ext/SpatialPlugin/graphdb/findGeometriesWithinDistance'
        jsonparam = dict()
        jsonparam['layer'] = layer
        jsonparam['pointX'] = x
        jsonparam['pointY'] = y
        jsonparam['distanceInKm'] = dist
        
        
        resp_json = json.loads(self.POST(self.__url + extraURL, jsonparam))
        
        return [each['data']['pgid'] for each in resp_json]
        
    
    def POST(self, url, json):
        
        resp = requests.post(url, json, auth=(wcon.NEO_USER, wcon.NEO_PSW)) 
        return resp.text
        
if __name__ == '__main__':
    sapi   = SpatialApi()
    
    #sapi.getLayer("geomlayer")
    print(sapi.findGeometriesWithinDistance('geomlayer', 8.0, 50.0, 500))