import ranking

class Matchmaking:
    def __init__(self, database_api=None):
        self.db = database_api
        self.ranking = ranking.Ranking(database=database_api)