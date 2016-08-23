from neoquery import NeoQuery
import classes.constant.neoconstant as neoc
from django.contrib.auth import get_user_model

class UserToNeo(NeoQuery):
    
    def __init__(self):
        super().__init__()
        
    
    def createCriteria(self, user ):
        node = self.db.nodes.create(email = user.email,
                        email_subs = user.email_subs,
                        language = user.language,
                        pgid = user.id,
                        )
        root = self.db.labels.create(neoc.LABEL_USER)
        root.add(node)
        
    def createUserToNeoByEmail(self, emailpar):
        user = get_user_model().objects.get(email=emailpar)
        result = self.getUserById(user.id)
        print('result',result)
        if result is not None and 0<len(result):
            return False
        else:
            print('create user to NEO')
            self.createCriteria(user)
            return True
    
        