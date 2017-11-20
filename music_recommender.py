from flask import Flask
from flask import request
from flask import render_template
import pandas as pd
import pandas as pd
import pymysql
from sqlalchemy import create_engine

app = Flask(__name__)
global recommendations

@app.route('/')
def my_form():
	global recommendations
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/music_recommender')
	recommendations = pd.read_sql_query('SELECT * FROM `recommendations`', engine)
	global top10Songs
	topSongs = pd.read_sql_query('SELECT * FROM `top1000Songs`', engine)
	top10Songs = topSongs.song_id[0:10].apply(str).tolist()
 	return render_template("my-form.html")

@app.route('/', methods=['POST'])
def my_form_post():
    uid = int(request.form['text'])
    global recommendations
    l = recommendations.query('uid == %i' %uid)
    prefix = "For you: <br/>"
    if not l.empty:
    	l = l.song_id.apply(str).tolist()
    else:
    	l = top10Songs
    	prefix = " Here are 10 most popular songs: <br/>"
    s =  prefix + '<br/>'.join(l)
    return s

if __name__ == '__main__':
 	app.run()