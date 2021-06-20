from flask import Flask
import api.database_api
import api.ranking

db = api.database_api.STF(
    username="demoauth",
    password="ZhJ3bGjgfoyL9chU284fRGSqPN9dXnypi2MFPLMokXkNKE2JGH",
    host="stf.nbti.net",
    database="stf"
)

rank = api.ranking(database=db)