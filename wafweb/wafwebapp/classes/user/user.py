

class User():
    
    def __init__(self):
        pass
    
    def setParameters(self, email_auth, email_subs = None, psw = None):
        
        self.email_auth=email_auth
        if email_subs is None:
            self.email_subs=email_auth
        else:
            self.email_subs=email_subs
        self.psw = psw
        self.hash = None