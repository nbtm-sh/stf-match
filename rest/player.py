class Player:
    def __init__(self, id=None, uName=None, uCountry=None):
        self.id = id
        self.uName = uName
        self.uCountry = uCountry
    
    def json(self):
        return {
            "id": self.id,
            "uName": self.uName,
            "uCountry": self.uCountry
        }