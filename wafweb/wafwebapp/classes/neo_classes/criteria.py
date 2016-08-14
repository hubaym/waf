

class Criteria():
    
    def __init__(self, departure,departureid,  arrival,arrivalid,
                 deptDistance=0.0, arrDistance=0.0,
                 userStatus = 'TEMP',saveStatus='NEW', userid = None, bothWay =True ):
        self.departure = departure
        self.departureid = departureid
        self.arrival = arrival
        self.arrivalid = arrivalid
        self.deptDistance = deptDistance
        self.arrDistance = arrDistance
        self.userStatus =userStatus
        self.saveStatus = saveStatus
        self.userid = userid
        self.bothWay = bothWay