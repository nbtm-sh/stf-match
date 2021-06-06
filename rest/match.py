class Match:
    def __init__(self, id=None, uPlayer1=None, uPlayer2=None, tDate=None, tRound=None, tResult=None, tRoundNick=None, tWeight=None, tTournament=None, tRoundGroup=None):
        self.id = id
        self.uPlayer1 = uPlayer1
        self.uPlayer2 = uPlayer2
        self.tRounds = []
        self.tWeight = tWeight
        self.tTournament = tTournament
        self.tFirstTo = None
        self.uPlatform = None
        self.tMatchType = None

        self.tDate = tDate
        self.tRound = tRound
        self.tRoundNick = tRoundNick
    
    def get_winner(self):
        win_count = self.get_win_count()
        p1_win_count = win_count[0]
        p2_win_count = win_count[1]
        
        return self.uPlayer1 if p1_win_count > p2_win_count else self.uPlayer2
    
    def get_win_count(self):
        p1_win_count = 0
        p2_win_count = 0

        for i in self.tRounds:
            p1_win_count += int(i.tWinner.id == self.uPlayer1.id)
            p2_win_count += int(i.tWinner.id == self.uPlayer2.id)
        
        return [p1_win_count, p2_win_count]
    

    def json(self):
        return {
            "id": self.id,
            "uPlayer1": self.uPlayer1.json(),
            "uPlayer2": self.uPlayer2.json(),

            "tDate": if self.tDate != None self.tDate.strftime('%Y-%m-%d %H:%M:%S') else None,
            "tRound": self.tRound,
            "tRounds": [i.json() for i in self.tRounds]
        }
    
    def add_fight(self, id, uPlayer1Fighter, uPlayer2Fighter, tMatchTime : int, tWinner : int, tSeq : int):
        append_object = Fight(
            id = id,
            uPlayer1 = self.uPlayer1,
            uPlayer2 = self.uPlayer2,
            uPlayer1Fighter = uPlayer1Fighter,
            uPlayer2Fighter = uPlayer2Fighter,
            tWinner = tWinner,
            tMatchTime = tMatchTime,
            tSeq = tSeq
        )
        
        self.tRounds.append(append_object)

class Tournament:
    def __init__(self, id=None, tName=None, tLocation=None, uParticipants=None):
        self.id = id
        self.tName = tName
        self.tLocation = tLocation
        self.uParticipants = uParticipants
    
    def json(self):
        return {
            "id": self.id,
            "tName": self.tName,
            "tLocation": self.tLocation
        }

class Fight:
    def __init__(self, id=None, uPlayer1=None, uPlayer2=None, uPlayer1Fighter=None, uPlayer2Fighter=None, tWinner=None, tSeq=None, tMatchTime=None):
        self.id = id
        self.uPlayer1 = uPlayer1
        self.uPlayer2 = uPlayer2
        self.uPlayer1Fighter = uPlayer1Fighter
        self.uPlayer2Fighter = uPlayer2Fighter
        self.tSeq = tSeq
        self.tMatchTime = tMatchTime
        self.tWinner = self.uPlayer1 if tWinner == 1 else self.uPlayer2

    def json(self):
        return {
            "id": self.id,
            "uPlayer1": self.uPlayer1.json(),
            "uPlayer2": self.uPlayer2.json(),
            "tSeq": self.tSeq,
            "tMatchTime": self.tMatchTime,
            "uPlayer1Fighter": self.uPlayer1Fighter,
            "uPlayer2Fighter": self.uPlayer2Fighter,
            "tWinner": self.tWinner.json()
        }