class Match:
    def __init__(self, id=None, uPlayer1=None, uPlayer2=None, uPlayer1Fighter=None, uPlayer2Fighter=None, tDate=None, tRound=None, tResult=None, tRoundNick=None):
        self.id = id
        self.uPlayer1 = uPlayer1
        self.uPlayer2 = uPlayer2
        self.rounds = []

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

        for i in self.rounds:
            p1_win_count += int(i.tWinner.id == self.uPlayer1.id)
            p2_win_count += int(i.tWinner.id == self.uPlayer2.id)
        
        return [p1_win_count, p2_win_count]
    

    def json(self):
        return {
            "id": self.id,
            "uPlayer1": self.uPlayer1.json(),
            "uPlayer2": self.uPlayer2.json(),
            "uPlayer1Fighter": self.uPlayer1Fighter,
            "uPlayer2Fighter": self.uPlayer2Fighter,

            "tDate": self.tDate.strftime('%Y-%m-%d %H:%M:%S'),
            "tRound": self.tRound,
            "tResult": self.tResult.json()
        }
    
class Fight:
    def __init__(self, id=None, uPlayer1=None, uPlayer2=None, uPlayer1Fighter=None, uPlayer2Fighter=None, tWinner=None, tSeq=None):
        self.id = id
        self.uPlayer1 = uPlayer1
        self.uPlayer2 = uPlayer2
        self.uPlayer1Fighter = uPlayer1Fighter
        self.uPlayer2Fighter = uPlayer2Fighter
        self.tSeq = tSeq
        self.tWinner = self.uPlayer1 if tWinner == 1 else self.uPlayer2

    def json(self):
        return {
            "id": self.id,
            "uPlayer1": self.uPlayer1.json(),
            "uPlayer2": self.uPlayer2.json(),
            "tSeq": self.tSeq,
            
        }