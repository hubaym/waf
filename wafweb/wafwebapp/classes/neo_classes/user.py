

class User:
    
    def __init__(self,email, email_subs,
                 pgid,
                 language = 'en', facebookid=None):
        self.email=email
        self.email_subs=email_subs
        self.language=language
        self.pgid = pgid
        self.facebookid = facebookid