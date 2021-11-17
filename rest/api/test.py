import database_api
import ranking
import time
import os

database = database_api.STF(
    username=os.environ["STF_USERNAME"],
    password=os.environ["STF_PASSWORD"],
    host="stf.nbti.net",
    database="stf"
)

#print(database.get_player(player_country="AU")[0].json())
#print(database.get_match(players=[1])[0].json())

ranker = ranking.Ranking(database=database)
t = database.get_tournament(id=1)[0]

v = ranker.all_ranking(update_database=True)
print("2nd call")
v = ranker.all_ranking()
print("Rank\tScore\tUsername")
v.sort(key=lambda x: x.uScore, reverse=True)
for i, c in zip(v, range(len(v))):
    print(f"#{c+1}\t{round(i.uScore, 2)}\t{i.uName}")
#print('\t' + '\n\t'.join([f"{x.uName}: {round(x.player_score, 9)}, Entries: {x.player_scores}" for x in v]))