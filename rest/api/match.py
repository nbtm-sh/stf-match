class Match:
    def __init__(self):
        self.id = None
        self.tTournament = None
        self.tRound = None
        self.tRoundGroup = None
        self.tRoundNick = None
        self.tFirstTo = None
        self.uPlatform = None
        self.tMatchType = None
        self.tMatchWeight = None
        self.uPlayer1 = None
        self.uPlayer2 = None
        self.tFights = []
    
    @staticmethod
    def parse(data, get_fights=True, get_players=True, database=None):
        return_object = Match()

        return_object.id = data[0]
        return_object.tTournament = data[1]
        return_object.tRound = data[2]
        return_object.tRoundGroup = data[3]
        return_object.tRoundNick = data[4]
        return_object.tFirstTo = data[5]
        return_object.uPlatform = data[6]
        return_object.tMatchType = data[7]
        return_object.tMatchWeight = data[8]
        return_object.uPlayer1 = data[9]
        return_object.uPlayer2 = data[10]
        return_object.uDq = 0 if data[11] == None else data[11]
        return_object.tBracket = data[12]

        if database != None:
            if get_players:
                return_object.uPlayer1 = database.get_player(player_id=return_object.uPlayer1)[0]
                return_object.uPlayer2 = database.get_player(player_id=return_object.uPlayer2)[0]
        
        if return_object.uDq & 0x1 == 1: # Bit offset 1
            return_object.uPlayer1.bQualified = False
        if return_object.uDq & 0x2 == 2: # Bit offset 2
            return_object.uPlayer2.bQualified = False
        
        return return_object
    
    def json(self):
        return {
            "id": self.id,
            "tTournament": self.tTournament,
            "tRound": self.tRound,
            "tRoundGroup": self.tRoundGroup,
            "tRoundNick": self.tRoundNick,
            "tFirstTo": self.tFirstTo,
            "uPlatform": self.uPlatform,
            "tMatchType": self.tMatchType,
            "tMatchWeight": self.tMatchWeight,
            "uPlayer1": self.uPlayer1.json() if type(self.uPlayer1) != int else self.uPlayer1,
            "uPlayer2": self.uPlayer2.json() if type(self.uPlayer2) != int else self.uPlayer2,
            "tRounds": [i.json() for i in self.tFights]
        }