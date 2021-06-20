from api.tournament import Tournament

class Ranking:
    def __init__(self, database=None):
        self.database = database
        self.players = []
    
    RETURN_OBJECT = 1
    RETURN_DICT = 2
    data_modified = True

    def update_player_routine(self, player):
        pass
    
    def all_ranking(self, update_database=False):
        if self.data_modified == True:
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
            
            if update_database:
                self.update_cache(None, players)
                self.data_modified = False
            return players
        else:
            query = "SELECT * FROM `playerScoresCache` WHERE `tTournament`=NULL"
    
    def tournament_exists_in_chache(self, tournament_id):
        # Check if the tournament results exist in the result cache

        query = f"SELECT * FROM `playerScoresCache` WHERE `tTournament`={tournament_id}"
        result = self.database.execute_query(query)

        return len(result) != 0
    
    def create_cache_index(self, tournament_id):
        # Get tournament entrants
        tournament = self.database.get_tournament(id=tournament_id)[0]
        tournament_entrants = []

        for i in tournament.tMatches:
            if i.uPlayer1.id not in tournament_entrants:
                tournament_entrants.append(i.uPlayer1.id)
            if i.uPlayer2.id not in tournament_entrants:
                tournament_entrants.append(i.uPlayer2.id)
        
        # Insert player list into database
        
        # Get last ID
        query = f"SELECT * FROM `playerScoresCache` ORDER BY `id` DESC LIMIT 1;"
        result = self.database.execute_query(query)[0]
        last_id = int(result[0])

        for i, c in zip(tournament_entrants, range(len(tournament_entrants))):
            query = f"INSERT INTO `playerScoresCache` (id, uPlayerId, uScore, tTournament) VALUES ({last_id + 1 + c}, {i}, 0, {tournament_id});"
            self.database.execute_query(query)
            print(query)
        
        self.database.database_connection.commit()

    def update_cache(self, tournamet_id, results):
        # Update the cache database
        # This can later be revised to have cache stored server side, instead of on the database
        for i in results:
            t = tournamet_id if tournamet_id != None else "NULL"
            query = f"UPDATE `playerScoresCache` SET `uScore`={round(i.uScore, 2)} WHERE `uPlayerId`={i.id} AND `tTournament`={t};"
            print(query)
            self.database.execute_query(query)
        
        self.database.database_connection.commit()

    def get_tournament_ranking(self, tournament_id, ret=RETURN_OBJECT, count_dq=False, update_database_on_data_change=False):
        # data_modified flag will signal that the data in the cache is no longer valid
        # this is true by default 
        if self.data_modified:
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
            
            if update_database_on_data_change:
                if not self.tournament_exists_in_chache(tournament_id):
                    self.create_cache_index(tournament_id)
                self.update_cache(tournament_id if type(tournament_id) != Tournament else tournament_id.id, players)
            return players
        else:
            # Get data from cache database
            query = f"SELECT * FROM `playerScoresCache` WHERE `tTournament`={tournament_id.id if type(tournament_id) == Tournament else tournament_id}"
            results = self.database.execute_query(query)

            # Get player objects from player ids and assign them a score
            players = []
            
            for i in results:
                player_id = i[1]
                player_obj = self.database.get_player(player_id=player_id)

                player_obj.uScore = i[2]
                players.append(players)