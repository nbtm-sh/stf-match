from tournament import Tournament

class Ranking:
    def __init__(self, database=None):
        self.database = database
        self.players = []
    
    RETURN_OBJECT = 1
    RETURN_DICT = 2

    def update_player_routine(self, player):
        pass
    
    def all_ranking(self, update_database=False):
        tournaments = self.database.get_tournament()
        players = []
        player_scores = {}
        player_tournament_count = {}

        def index(lst, uname):
            for i in range(len(lst)):
                if lst[i].uName == uname:
                    return i
            
            return -1

        for tournament in tournaments:
            tournament_results = self.get_tournament_ranking(tournament, ret=self.RETURN_OBJECT, count_dq=False)

            for player in tournament_results:
                if player.uName not in player_tournament_count.keys():
                    player_tournament_count[player.uName] = 0
                    player_scores[player.uName] = 0
                player_tournament_count[player.uName] += 1
                player_scores[player.uName] += player.uScore

                if index(players, player.uName) == -1:
                    players.append(player)
        
        for i in list(player_scores.keys()):
            if player_scores[i] != 0: # Do not consider players with no score
                player_scores[i] += 3
                player_scores[i] += 0
            # Solve the issue where new players will jump to the top of the leaderboard
            player_scores[i] /= (player_tournament_count[i] + 2)
            players[index(players, i)].score = player_scores[i]
        
        return players

    

    def get_tournament_ranking(self, tournament_id, ret=RETURN_OBJECT, count_dq=False):
        if type(tournament_id) != Tournament:
            matches = self.database.get_tournament(id=tournament_id)[0].tMatches
        else:
            matches = tournament_id.tMatches

        players = []
        player_scores = {}

        for i in matches:
            if i.uPlayer1.uName not in list(player_scores.keys()):
                player_scores[i.uPlayer1.uName] = 0
                players.append(i.uPlayer1)
            if i.uPlayer2.uName not in list(player_scores.keys()):
                player_scores[i.uPlayer2.uName] = 0
                players.append(i.uPlayer2)
            
            for f in i.tFights:
                player_scores[i.uPlayer1.uName] += round(i.tMatchWeight * int(f.tWinner == i.uPlayer1.id) * int(not (i.uPlayer1.uIgnore & count_dq)), 2)
                player_scores[i.uPlayer2.uName] += round(i.tMatchWeight * int(f.tWinner == i.uPlayer2.id) * int(not (i.uPlayer2.uIgnore & count_dq)), 2)
        
        # Remove disqualified players
        if ret == self.RETURN_DICT:
            return player_scores
        
        for i in range(len(players)):
            players[i].uScore = player_scores[players[i].uName]
            players[i].bIgnore = players[i].uIgnore
        
        return players