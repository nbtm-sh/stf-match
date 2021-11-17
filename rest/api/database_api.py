import mysql.connector
from player import Player
from tournament import Tournament
from match import Match
from fight import Fight
from ranking import Ranking

class STF:
    def __init__(self, username=None, password=None, host=None, database=None):
        self.database_connection = mysql.connector.connect(
            username=username,
            password=password,
            host=host,
            database=database
        )
        self.ranker = Ranking(database=self)

    def execute_query(self, query):
        cursor = self.database_connection.cursor()
        cursor.execute(query)

        return cursor.fetchall()
    
    def set_player_score(self, player_id, score, tournament=None): # Requires authenticated user
        query = f"UPDATE `playerScoresCache` SET `uScore`={round(score, 2)} WHERE `uPlayerId`={player_id}"
        if tournament != None:
            query += f" AND `tTournament`={tournament}"
        query += ";"
        self.execute_query(query)
        self.database_connection.commit()
    
    def get_all_player_rankings(self, tournament=None):
        ranking = self.ranker.all_ranking()
        ranking = [i.json() for i in ranking]

        return ranking

    def get_player(self, player_id=None, player_country=None, player_username=None, player_team=None):
        query = "SELECT * FROM `players`"
        values = {
            "id": player_id,
            "uName": player_username,
            "uCountry": player_country,
            "uTeam": player_team
        }

        append_keys = []
        append_values = []

        for k, v in zip(values.keys(), values.values()):
            if v != None:
                append_keys.append(k)
                append_values.append(v)
        
        if len(append_keys) > 0:
            query += " WHERE "

        # Create query

        for i in range(len(append_keys)):
            if i > 0:
                query += " AND "
            append_chars = '"' if type(append_values[i]) == str else ''
            query += f" `{append_keys[i]}`={append_chars}{append_values[i]}{append_chars}"
        
        if query == "SELECT * FROM `players` WHERE ":
            query.replace(" WHERE ", "")
        
        query_result = self.execute_query(query)
        if len(query_result) == 0:
            return
        
        query_result = query_result
        return [Player.parse(i) for i in query_result]
    
    def get_fights(self, id=None, player1_fighter=None, player2_fighter=None, tournament=None, match=None, seq=None, winner=None):
        query = "SELECT * FROM `individualMatches` WHERE "

        appended_values = 0
        if id != None:
            query += f"`id`={id}"
            appended_values += 1
        
        if player1_fighter != None:
            if appended_values > 0:
                query += " AND "
            query += f"`uPlayer1Fighter`=\"{player1_fighter}\""
            appended_values += 1
        
        if player2_fighter != None:
            if appended_values > 0:
                query += " AND "
            query += f"`uPlayer2Fighter`=\"{player2_fighter}\""
            appended_values += 1
        
        if tournament != None:
            if appended_values > 0:
                query += " AND "
            query += f"`tTournament`=\"{tournament}\""
            appended_values += 1
        
        if match != None:
            if appended_values > 0:
                query += " AND "
            query += f"`tMatch`=\"{match}\""
            appended_values += 1
        
        if query == "SELECT * FROM `individualMatches` WHERE ":
            query.replace(" WHERE ", "")
        
        query += ";"
        
        query_result = self.execute_query(query)
        if len(query_result) == 0:
            return
        
        query_result = query_result
        return [Fight.parse(i) for i in query_result]

    def get_match(self, players=None, fighters=None, tournament=None, id=None):
        query = "SELECT * FROM `matches` WHERE "

        try:
            players.remove(None)
            players.remove(None)
        except:
            pass
        
        appended_values = 0

        if id != None:
            query += f"`id`={id}"
            appended_values += 1
        
        if tournament != None:
            if appended_values > 0:
                query += " AND "
            appended_values += 1
            query += f"`tTournament`={tournament}"
        print(query)
        if players != None and len(players) != 0:
            appended_values += 1
            if appended_values > 0:
                query += " AND "
            if len(players) == 1:
                query += f"(`uPlayer1`={players[0]} OR `uPlayer2`={players[0]})"
            elif len(players) == 2:
                query += f"((`uPlayer1`={players[0]} OR `uPlayer2`={players[0]}) AND (`uPlayer1`={players[1]} OR `uPlayer2`={players[1]}))"
        
        if query.endswith(" WHERE "):
            query = query.replace(" WHERE " , "")
        print(query)
        query += ";"

        query_result = self.execute_query(query)
        if len(query_result) == 0:
            return
        
        return_object = [Match.parse(i, database=self) for i in query_result]
        
        for i in range(len(return_object)):
            return_object[i].tFights = self.get_fights(match=return_object[i].tRound, tournament=tournament)
            return_object[i].tFights.sort(key=lambda x: x.tSeq)
        
        return return_object
    
    def get_tournament(self, id=None, name=None, location=None):
        query = "SELECT * FROM `tournaments` WHERE "
        appended_values = 0

        if id != None:
            query += f"`id`={id}"
            appended_values += 1
        
        if name != None:
            if appended_values > 0:
                query += " AND "
            query += f"`tName`=\"{name}\""
        
        if location != None:
            if appended_values > 0:
                query += " AND "
            query += f"`tLocation`={location}"
        
        if appended_values == 0:
            query = query.replace(" WHERE ", "")
        query += ";"

        query_result = self.execute_query(query)
        if len(query_result) == 0:
            return
        
        return_object = [Tournament.parse(i, database=self) for i in query_result]
        return return_object