from flask import Flask
from flask import render_template, redirect, url_for, request, session
from flask_bootstrap import Bootstrap
import random
import spotipy
import sys
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import json


scope = 'user-library-read'

spotify = spotipy.Spotify()


app = Flask(__name__)
app.secret_key = 'You Will Never Guess'

Bootstrap(app)

@app.route("/home", methods=['GET','POST'])
def hello_world():
        if request.method == "GET":
		session['codes'] = ['chill', 'happy', 'emo', 'lit', 'basic', 'unique']
		session['userCount'] = 0

		session['users'] = []
		session['minPopular'] = 100000
		session['maxPopular'] = 0
		session['minDanceability'] = 1
		session['maxDanceability'] = 0
		session['minValence'] = 1
		session['maxValence'] = 0 
		session['minInstrumental'] = 1 
		session['maxInstrumental'] = 0
		session['minAcoustic'] = 1
		session['maxAcoustic'] = 0
		session['maxLit'] = 0
		session['maxChill'] = 0
		session['mostBasic'] = ""
		session['mostUnique'] = ""
		session['mostEmo'] = ""
		session['mostHappy'] = ""
		session['mostLit'] = ""
		session['mostChill'] = ""
		
    		return render_template("index.html", count=session['userCount'])
	if request.method == "POST":
		username = request.form['username']
		session['users'].append(username)
		token = util.prompt_for_user_token(username, scope,client_id='04b743a8c3714b37a04cad2f516518af',client_secret='ee75f1b3dc774da0a921a8a8c10b0cac',redirect_uri = 'http://www.cs.cmu.edu/~15251/schedule.html')
		tracks = []
		energyTotal = 0
		popularTotal = 0
		danceabilityTotal = 0
		valenceTotal = 0
		instrumentalnessTotal = 0
		acousticnessTotal = 0

		if token:
			sp = spotipy.Spotify(auth=token)
			results = sp.current_user_saved_tracks()
			tids = []
			counter = 0
			for t in (results['items']):
				print("popularity",t['track']['popularity'])
				popularTotal+=t['track']['popularity']
				tids.append(t['track']['uri'])
				features = sp.audio_features(tids)
				currentFeature = features[counter]
				#energy = features[len(tids)-1]['energy']
				energyTotal+=features[counter]['energy']
				danceabilityTotal+=features[counter]['danceability']
				valenceTotal+=features[counter]['valence']
				instrumentalnessTotal+=features[counter]['instrumentalness']
				acousticnessTotal+=features[counter]['acousticness']
				counter+=1
		else:
		    print "Can't get token for", username
		if popularTotal < session['minPopular']:
			session['mostUnique'] = username
			session['minPopular'] = popularTotal
		if popularTotal > session['maxPopular']:
			session['mostBasic'] = username
			session['maxPopular'] = popularTotal
		if danceabilityTotal + energyTotal > session['maxLit']:
			session['maxLit'] = danceabilityTotal + energyTotal
			session['mostLit'] = username
		if valenceTotal < session['minValence']:
			session['minValence'] = valenceTotal
			session['mostEmo'] = username
		if valenceTotal > session['maxValence']:
			session['maxValence'] = valenceTotal
			session['mostHappy'] = username
		if acousticnessTotal > session['maxChill']:
			session['maxChill'] = acousticnessTotal
			session['mostChill'] = username
		session['userCount'] +=1
		session['questions']= {
			"chill":session['mostChill'],
			"happy":session['mostHappy'],
			"emo":session['mostEmo'],
			"lit":session['mostLit'],
			"basic":session['mostBasic'],
			"unique":session['mostUnique'],
		}
		if (session['userCount']==2):
			return render_template("instructions.html")
		return render_template("index.html")

@app.route("/calculations", methods=['GET', 'POST'])
def calc():
	#do stuff
	return render_template("instructions.html")


@app.route("/mostLikely", methods=['GET', 'POST'])
def play():
	if request.method == "GET":
		questions = session['questions']
		print(questions)
		codes = session['codes']
		rand = random.randint(0,5)
		if rand==2:
			rand = 3
		print(rand)
		session['currq'] = session['codes'][rand]
		session['curra'] = session['questions'].get(codes[rand])
		print(session['curra'])
		return render_template("mostLikely.html", question=codes[rand], u1 = session['users'][0], u2 = session['users'][1])
		#session['uname'] = request.form['uname']
		#if session['uname'] == session['curra']:
		#	return render_template("results.html", message="Congrats, that's correct!")

@app.route("/results", methods=['GET', 'POST'])
def res():
	session['uname'] = request.form['submitbutton']
	print(session['uname'])
	print(session['curra'])
	
	#return render_template("results.html", message=message)
	if session['uname'] == session['curra']:
		return render_template("results.html", message="Congrats, that's correct!")
	else:
		return render_template("results.html", message="No, sorry, the actual answer was "+session['curra'])
	#return render_template("results.html", message="No, sorry, the actual answer was "+session['curra'])

