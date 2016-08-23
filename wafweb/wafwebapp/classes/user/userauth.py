import bcrypt
from userdbconnection import UserDbConnection

class UserAuth():
    
    def __init__(self):
        self.db = UserDbConnection()
    
    def checkPass(self, user, password):
        try:
            userhash = bytearray(self.db.getHashforUser(user.email_auth))
        except Exception as s:
            raise s
        if userhash == bcrypt.hashpw(password.encode('ascii'), userhash):
            return True
        else:   
            return False
        
        
    def registrateWithEmail(self, user):
        
        if user.psw is not None:
            try:
                user.psw = user.psw.encode('ascii')
            except Exception as a:
                print(a)
            hashgen = bcrypt.hashpw(user.psw, bcrypt.gensalt())
            user.hash = hashgen
        self.db.insertNewUser(user)
        
    def registrateWithFB(self, user):
        
        if user.psw is not None:
            try:
                user.psw = user.psw.encode('ascii')
            except Exception as a:
                print(a)
            hashgen = bcrypt.hashpw(user.psw, bcrypt.gensalt())
            user.hash = hashgen
        self.db.insertNewUser(user)

        
        
if __name__ == "__main__":
    #print(type(bcrypt.hashpw('hello'.encode('ascii'), bcrypt.gensalt())))
    #print(bcrypt.hashpw('hello'.encode('ascii'), bcrypt.gensalt()))
    #user =User()
    #user.setParameters("hellobello2", psw='bas')
    #aut = UserAuth()
    #aut.registrateWithEmail(user)
    
    #print(aut.checkPass(user,'bas2'))
    #user = UserProfile.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    
        
        