class Player:
    def __init__(self):
        self.id = None
        self.uName = None
        self.uCountry = None
        self.uTeam = None
        self.bQualified = True
        self.uScore = 0
        self.bIgnore = False
    
    @staticmethod
    def parse(data):
        return_object = Player()
        return_object.id = data[0]
        return_object.uName = data[1]
        return_object.uCountry = data[2]
        return_object.uTeam = data[3]
        return_object.uJoinDate = data[4]
        return_object.uIgnore = bool(data[5])

        return return_object
    
    def json(self):
        return {
            "id": self.id,
            "uName": self.uName,
            "uCountry": self.uCountry,
            "uTeam": self.uTeam,
            "bQualified": self.bQualified,
            "uScore": self.uScore,
            "bIgnore": self.bQualified
        }