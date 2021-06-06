import mysql.connector
from player import Player
from match import Match, Fight, Tournament
import datetime

class SQLAPI:
    database_connection = None

    def __init__(self, host, username, password, database):
        self.database_connection = mysql.connector.connect(
            host=host,
            username=username,
            password=password,
            database=database
        )

    @staticmethod
    def parse_player(data):
        result_object = Player()

        for i in data:
            result_object.id = i[0]
            result_object.uName = i[1]
            result_object.uCountry = i[2]
            result_object.qualified = (result_object.id > 0)
        
        return result_object
    
    def parse_match(self, data, exclude_tournament=False):
        result_object = Match()

        for i in data:
            result_object.id = i[0]
            result_object.tTournament = self.get_tournament_by_id(i[1], exclude_matches=True)
            result_object.tRound = i[2]
            result_object.tRoundNick = i[4]
            result_object.tFirstTo = i[5]
            result_object.uPlatform = i[6]
            result_object.tMatchType = i[7]
            result_object.tWeight = i[8]
            result_object.uPlayer1 = self.get_player_by_id(i[9])
            result_object.uPlayer2 = self.get_player_by_id(i[10])
            result_object.tRounds = self.get_fights_by_match(i[0])
        
            # Collect rounds
        
        return result_object

    def parse_fights(self, data):
        result_object = []

        for i in data:
            new_obj = Fight()
            new_obj.id = i[0]
            new_obj.uPlayer1Fighter = i[1]
            new_obj.uPlayer2Fighter = i[2]
            new_obj.uPlayer1 = self.get_match_players(i[5])[0]
            new_obj.uPlayer2 = self.get_match_players(i[5])[1]
            new_obj.tSeq = i[6]
            new_obj.tWinner = new_obj.uPlayer1 if i[7] == 1 else new_obj.uPlayer2

            result_object.append(new_obj)
        
        result_object.sort(key=lambda x: x.tSeq, reverse=False)
        return result_object

    def parse_tournament(self, data, exculde_matches=False):
        result_object = Tournament()

        for i in data:
            result_object.id = i[0]
            result_object.tName = i[1]
            result_object.tLocation = i[2]
            result_object.uParticipants = self.get_tournament_participants(result_object)

        
        return result_object
    
    def get_tournament_participants(self, tournament : Tournament):
        t_id = tournament.id
        query = f"SELECT * FROM `matches` WHERE `tTournament`={str(t_id)};"

        cursor = self.database_connection.cursor()
        cursor.execute(query)

        results = cursor.fetchall()

        # Collect user IDs
        user_ids = []

        for i in results:
            if i[9] not in user_ids:
                user_ids.append(i[9])
            if i[10] not in user_ids:
                user_ids.append(i[10])
        
        users = []
        for i in user_ids:
            users.append(self.get_player_by_id(i))
        
        return users

    def get_matches_by_tournament(self, tournament : Tournament):
        query = f"SELECT * FROM `matches` WHERE `tTournament`={tournament.id};"

        cursor = self.database_connection.cursor()
        cursor.execute(query)

        results = cursor.fetchall()

        return_data = []
        for i in results:
            return_data.append(self.parse_match(i, exclude_tournament=True))
        
        return return_data

    def get_all_tournaments(self):
        query = "SELECT * FROM `tournaments`;"

        cursor = self.database_connection.cursor()
        cursor.execute(query)

        results = cursor.fetchall()

        return_data = []
        for i in results:
            return_data.append(self.parse_tournament([i]))
        
        return return_data

    def get_tournament_by_id(self, tournament_id, exclude_matches=False):
        query = f"SELECT * FROM `tournaments` WHERE `id`={str(tournament_id)};"

        cursor = self.database_connection.cursor()
        cursor.execute(query)

        results = cursor.fetchall()
        return self.parse_tournament(results, exclude_matches)

    def get_player_by_id(self, _id):
        query = f"SELECT * FROM `players` WHERE `id`={str(abs(_id))};"

        cursor = self.database_connection.cursor()
        cursor.execute(query)

        results = cursor.fetchall()
        return SQLAPI.parse_player(results)
    
    def get_player_by_username(self, username):
        query = f"SELECT * FROM `players` WHERE `uName`=\"{username}\";"

        cursor = self.database_connection.cursor()
        cursor.execute(query)

        results = cursor.fetchall()
        return SQLAPI.parse_player(results)
    
    def get_fight(self, fight_id):
        query = f"SELECT * FROM `individualMatches` WHERE `id`={str(fight_id)};"
        
        cursor = self.database_connection.cursor()
        cursor.execute(query)

        results = cursor.fetchall()
        return self.parse_fights(results)
    
    def get_match_by_id(self, match_id):
        query = f"SELECT * FROM `matches` WHERE `id`={str(match_id)};"

        cursor = self.database_connection.cursor()
        cursor.execute(query)

        results = cursor.fetchall()
        return self.parse_match(results)
    
    def get_fights_by_match(self, match_id):
        query = f"SELECT * FROM `individualMatches` WHERE `tMatch`={str(match_id)}"

        cursor = self.database_connection.cursor()
        cursor.execute(query)

        results = cursor.fetchall()
        return self.parse_fights(results)
    
    def get_match_players(self, match_id):
        query = f"SELECT uPlayer1, uPlayer2 FROM `matches` WHERE `id`={str(match_id)};"
        
        cursor = self.database_connection.cursor()
        cursor.execute(query)

        results = cursor.fetchall()[0]

        return [self.get_player_by_id(results[0]), self.get_player_by_id(results[1])]
    
    def get_match_by_players(self, player1, player2):
        query = f"SELECT * FROM `matches` WHERE (`uPlayer1`={player1.id} OR `uPlayer2`={player1.id}) AND (`uPlayer1`={player2.id} or `uPlayer2`={player2.id});"

        cursor = self.database_connection.cursor()
        cursor.execute(query)

        results = cursor.fetchall()
        return_data = []
        for i in results:
            return_data.append(self.parse_match(i, exclude_tournament=True))
        
        return return_data