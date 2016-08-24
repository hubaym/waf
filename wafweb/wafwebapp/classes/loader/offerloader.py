from offerstoneo import OffersToNeo
from offer import Offer
from mongolayer import MongoLayer
from waflog import WafLog
import status


class OfferLoader():
    
    def __init__(self):
        self.__mongo = MongoLayer()
        self.__neo = OffersToNeo()


    def initOffers(self):
        self.offers = self.__mongo.getOffersWithPlace()
        
    def initEvaluatedOffers(self):
        self.offers = self.__mongo.getEvaluatedOffers()
    
    def loadOffer(self):   
        self.initOffers()
        i = 0
        for offer in self.offers:
            offer = Offer(str(offer.get('_id')), 
                          offer.get('tweet_id'), 
                          offer.get('dept'),
                          offer.get('arr'),
                          offer.get('created_at'),
                          offer.get('text'),
                          offer.get('language'),
                          offer.get('source_level1'),
                          offer.get('source_level2'),
                          offer.get('links'),
                          status.TWITTER_IN_NEO_EMAIL_NOT_DONE
                  )
            #WafLog().neologger.info(str(offer.__dict__).encode('utf-8'))
            self.__neo.createOffer(offer)
            i+=1
            if i%200 ==0:
                WafLog().neologger.info('relationship created  {0}'.format(i))
        WafLog().neologger.info('Loading offers - finished')
    
    def deleteOffersfromNeo(self):
        self.__neo.deleteOffers()
          


if __name__ == '__main__':
    print('start to load offers to neo')
    toneo = OfferLoader()
    toneo.deleteOffersfromNeo()
    toneo.loadOffer()
    print('job is done')
   
    
    