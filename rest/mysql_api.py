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
            print(i)
            result_object.id = i[0]
            result_object.uName = i[1]
            result_object.uCountry = i[2]
            result_object.qualified = (result_object.id > 0)
        
        return result_object

    def parse_fight(self, data):
        result_object = Fight()

        for i in data:
            result_object.id = i[0]
            result_object.uPlayer1Fighter = self.get_player_by_id(i[1])
            result_object.uPlayer2Fighter = self.get_player_by_id(i[2])
            result_object.uPlayer1 = self.get_match_players(i[5])[0]
            result_object.uPlayer2 = self.get_match_players(i[5])[1]
            result_object.tSeq = i[6]
            result_object.tWinner = result_object.uPlayer1 if i[7] == 1 else result_object.uPlayer2

        
        return result_object

    def parse_tournament(self, data):
        result_object = Tournament()

        for i in data:
            result_object.id = i[0]
            result_object.tName = i[1]
            result_object.tLocation = i[2]
        
        return result_object

    def get_all_tournaments(self):
        query = "SELECT * FROM `tournaments`;"

        cursor = self.database_connection.cursor()
        cursor.execute(query)

        results = cursor.fetchall()

        return_data = []
        for i in results:
            return_data.append(self.parse_tournament([i]))
        
        return return_data

    def get_tournament(self, tournament_id):
        query = f"SELECT * FROM `tournaments` WHERE `id`={str(tournament_id)};"

        cursor = self.database_connection.cursor()
        cursor.execute(query)

        results = cursor.fetchall()
        return self.parse_tournament(results)

    def get_player_by_id(self, _id):
        query = f"SELECT * FROM `players` WHERE `id`={str(abs(_id))};"

        cursor = self.database_connection.cursor()
        cursor.execute(query)

        results = cursor.fetchall()
        return SQLAPI.parse_player(results)
    
    def get_player_by_username(self, username):
        query = f"SELECT * FROM `players` WHERE `uName`={username};"

        cursor = self.database_connection.cursor()
        cursor.execute(query)

        results = cursor.fetchall()
        return SQLAPI.parse_player(results)
    
    def get_fight(self, fight_id):
        query = f"SELECT * FROM `individualMatches` WHERE `id`={str(fight_id)};"
        
        cursor = self.database_connection.cursor()
        cursor.execute(query)

        results = cursor.fetchall()

    
    def get_all_matches(self):
        query = "SELECT * FROM `matches`"
        match_object = []
    
    def get_match_players(self, match_id):
        query = f"SELECT uPlayer1, uPlayer2 FROM `matches` WHERE `id`={str(match_id)};"
        
        cursor = self.database_connection.cursor()
        cursor.execute(query)

        results = cursor.fetchall()[0]

        return [self.get_player_by_id(results[0]), self.get_player_by_id(results[1])]