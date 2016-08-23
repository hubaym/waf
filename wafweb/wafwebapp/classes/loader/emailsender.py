from classes.neo_classes.neoquery import NeoQuery


class EmailSender():
    
    def __init__(self):
        self.neo = NeoQuery()
        
    
    def proccessTask(self):
            
        self.getEmailsandOffersFromDB()
        self.sendEmails()
        
        
    def getEmailsandOffersFromDB(self):
        self.neo
        
        pass
    
    def sendEmails(self):
        pass