class Tournament:
    def __init__(self):
        self.id = None
        self.tName = None
        self.tLocation = None
        self.tMatches = None
    
    @staticmethod
    def parse(data, database=None, get_matches=True):
        return_object = Tournament()
        return_object.id = data[0]
        return_object.tName = data[1]
        return_object.tLocation = data[2]
        return_object.tMatches = None

        if database != None:
            if get_matches:
                return_object.tMatches = database.get_match(tournament=return_object.id)
        
        return return_object
    
    def json(self):
        return {
            "id": self.id,
            "tName": self.tName,
            "tLocation": self.tLocation,
            "tMatches": [i.json() for i in self.tMatches] if self.tMatches != None else None
        }