import mysql.connector
from player import Player
from match import Match
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
    
    def get_players_by_id(self, ids):
        """ Return player objects of the matching ids.
        Multiple IDs can be suplied via a list """
        if type(ids) != list:
            ids = [ids]
        
        query = f"SELECT * FROM `players` WHERE "
        for i in range(len(ids)):
            if (i >= 1 & i+1 != len(ids)):
                query += " OR "
            query += "`id`=" + str(ids[i])
        query += ";"
        cursor = self.database_connection.cursor()
        cursor.execute(query)

        result = cursor.fetchall()
        results = []
        for i in result:
            results.append(Player(
                id=i[0],
                uName=i[1],
                uCountry=i[2]
                ))
        
        return results
    
    def get_players_by_username(self, usernames):
        """ Return player objects of the matching usernames.
        Multiple usernames can be suplied via a list """
        if type(usernames) != list:
            usernames = [usernames]
        
        query = f"SELECT * FROM `players` WHERE "
        for i in range(len(usernames)):
            if (i >= 1 & i+1 != len(usernames)):
                query += " OR "
            query += "`uName`=\"" + str(usernames[i]) + "\""
        query += ";"

        cursor = self.database_connection.cursor()
        cursor.execute(query)

        result = cursor.fetchall()
        results = []
        for i in result:
            results.append(Player(
                id=i[0],
                uName=i[1],
                uCountry=i[2]
                ))
        
        return results
    
    def get_players_by_country(self, countries):
        """ Return player objects of the matching usernames.
        Multiple usernames can be suplied via a list """
        if type(countries) != list:
            countries = [countries]
        
        query = f"SELECT * FROM `players` WHERE "
        for i in range(len(countries)):
            if (i >= 1 & i+1 != len(countries)):
                query += " OR "
            query += "`uName`=\"" + str(countries[i]) + "\""
        query += ";"

        cursor = self.database_connection.cursor()
        cursor.execute(query)

        result = cursor.fetchall()
        results = []
        for i in result:
            results.append(Player(
                id=i[0],
                uName=i[1],
                uCountry=i[2]
                ))
        
        return results
    
    def get_players(self):
        """ Return player objects of the matching usernames.
        Multiple usernames can be suplied via a list """
        
        query = f"SELECT * FROM `players`;"
        cursor = self.database_connection.cursor()
        cursor.execute(query)

        result = cursor.fetchall()
        results = []
        for i in result:
            results.append(Player(
                id=i[0],
                uName=i[1],
                uCountry=i[2]
                ))
        
        return results
    
    def update_player(self, username=None, country=None):
        query = "UPDATE `players` ("
        append_data = []
        append_values = []

        if username != None:
            append_data.append("`uName`")rounds
            append_values.append("\"" + username + "\"")
        if country != None:
            append_data.append("`uCountry`")
            append_values.append("\"" + country + "\"")
        
        query += ", ".join(append_data)
        query += ") VALUES ("
        query += ", ".join(append_values)
        query += ")"

        cursor = self.database_connection.cursor()
        cursor.execute(query)
    
    def get_last_id(self, table):
        query = f"SELECT `id` FROM `{table}` ORDER BY `id` desc;"
        
        cursor = self.database_connection.cursor()
        cursor.execute(query)

        result = cursor.fetchall()

        return result[0][0]

    def create_player(self, username, country):
        query = f"INSERT INTO `players` (`id`, `uName`, `uCountry`) VALUES ({self.get_last_id('players')}, \"{username}\", \"{country}\");"

        cursor = self.database_connection.cursor()
        cursor.execute(query)
    
    def get_matches(self, query="SELECT * FROM `matches`;"):
        """ Get all matches """

        cursor = self.database_connection.cursor()
        cursor.execute(query)

        results = cursor.fetchall()
        result_objects = []

        # Warning!! Hacky shit ahead
        # Instead of adding a new column to the database
        # Make the id negative to indicate that the player was disqualified from the match

        dq_index_1 = []
        dq_index_2 = []

        x = 0
        for i in results:
            if i[1] < 0:
                dq_index_1.append(x)
            if i[2] < 0:
                dq_index_2.append(x)
            
            result_objects.append(Match(
                i[0],
                self.get_players_by_id(abs(i[1]))[0],
                self.get_players_by_id(abs(i[2]))[0],
                i[3],
                i[4],
                datetime.datetime.now() if i[5] == None else datetime.datetime.strptime(i[4], '%Y-%m-%d %H:%M:%S'),
                i[6],
                i[7]
                ))
        for i in dq_index_1:
            result_objects[i].uPlayer1.qualified = False

        for i in dq_index_2:
            result_objects[i].uPlayer2.qualified = False
        
        return result_objects
    
    def get_matchups(self, u1, u2):
        return self.get_matches(f"SELECT * FROM `matches` WHERE (`uPlayer1`={u1.id} OR `uPlayer2`={u1.id}) AND (`uPlayer1`={u2.id} or `uPlayer2`={u2.id});")
    
    def get_matches_played_by(self, u1):
        return self.get_matches(f"SELECT * FROM `matches` WHERE `uPlayer1`={u1.id} OR `uPlayer2`={u1.id};")
    
    def get_all_matches(self):
        return self.get_matches("SELECT * FROM `matches`;")