class Match:
    def __init__(self, id=None, uPlayer1=None, uPlayer2=None, uPlayer1Fighter=None, uPlayer2Fighter=None, tDate=None, tRound=None, tResult=None):
        self.id = id
        self.uPlayer1 = uPlayer1
        self.uPlayer2 = uPlayer2
        self.uPlayer1Fighter = uPlayer1Fighter
        self.uPlayer2Fighter = uPlayer2Fighter

        self.tDate = tDate
        self.tRound = tRound
        self.tResult = uPlayer1 if tResult == 1 else uPlayer2

    def json(self):
        return {
            "id": self.id,
            "uPlayer1": self.uPlayer1.json(),
            "uPlayer2": self.uPlayer2.json(),
            "uPlayer1Fighter": self.uPlayer1Fighter,
            "uPlayer2Fighter": self.uPlayer2Fighter,

            "tDate": self.tDate.strftime('%Y-%m-%d %H:%M:%S'),
            "tRound": self.tRound,
            "tResult": self.tResult.id
        }