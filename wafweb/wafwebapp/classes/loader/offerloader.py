from offerstoneo import OffersToNeo
from offer import Offer
from mongolayer import MongoLayer
from waflog import WafLog


class OfferLoader():
    
    def __init__(self):
        self.__mongo = MongoLayer()
        self.__neo = OffersToNeo()


    def initOffers(self):
        self.offers = self.__mongo.getOffersWithPlace()
    
    def loadOffer(self):   
        self.initOffers()
        i = 0
        for offer in self.offers:
            offer = Offer(str(offer.get('_id')), offer.get('tweet_id'), offer.get('dept'),
                  offer.get('arr'),
                  offer.get('created_at'),
                  offer.get('text'),
                  offer.get('language'),
                  offer.get('source_level1'),
                  offer.get('source_level2')
                  )
            WafLog().neologger.info(str(offer.__dict__).encode('utf-8'))
            self.__neo.createOffer(offer)
            i+=1
            if i%200 ==0:
                WafLog().neologger.info('relationship created  {0}'.format(i))
        WafLog().neologger.info('Loading offers - finished')
    
    def deleteOffersfromNeo(self):
        self.__neo.deleteOffers()
          


if __name__ == '__main__':
    toneo = OfferLoader()
    toneo.deleteOffersfromNeo()
    toneo.loadOffer()
   
    
    