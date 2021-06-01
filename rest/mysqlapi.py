import mysql.connector
from player import Player

class SQLAPI:
    database_connection = None

    def __init__(self, host, username, password, database):
        self.database_connection = mysql.connector.connect(
            host=host,
            username=username,
            password=password,
            database=database
        )
    
    def getPlayersById(self, ids):
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

        print(query)

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
    
    def getPlayersByUsername(self, usernames):
        """ Return player objects of the matching usernames.
        Multiple usernames can be suplied via a list """
        if type(usernames) != list:
            usernames = [usernames]
        
        query = f"SELECT * FROM `players` WHERE "
        for i in range(len(usernames)):
            if (i >= 1 & i+1 != len(usernames)):
                query += " OR "
            query += "`uName`=" + str(usernames[i])
        query += ";"

        print(query)

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