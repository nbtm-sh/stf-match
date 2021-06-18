class Fight:
    def __init__(self):
        self.id = None
        self.uPlayer1Fighter = None
        self.uPlayer2Fighter = None
        self.tDate = None
        self.tTournament = None
        self.tMatch = None
        self.tSeq = None
        self.tWinner = None
        self.tMatchTime = None
    
    @staticmethod
    def parse(data):
        return_object = Fight()

        return_object.id = data[0]
        return_object.uPlayer1Fighter = data[1]
        return_object.uPlayer2Fighter = data[2]
        return_object.tDate = data[3]
        return_object.tTournament = data[4]
        return_object.tMatch = data[5]
        return_object.tSeq = data[6]
        return_object.tWinner = data[7]
        return_object.tMatchTime = data[8]

        return return_object
    
    def json(self):
        return {
            "id": self.id,
            "uPlayer1Fighter": self.uPlayer1Fighter,
            "uPlayer2Fighter": self.uPlayer2Fighter,
            "tDate": self.tDate,
            "tTournament": self.tTournament,
            "tMatch": self.tMatch,
            "tSeq": self.tSeq,
            "tWinner": self.tWinner,
            "tMatchTime": self.tMatchTime
        }