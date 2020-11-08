from flask import Flask, render_template, request
app = Flask(__name__, template_folder='templates')
import sqlite3
# Retrieve data from database
def getData():
	conn=sqlite3.connect('/home/pi/interbrew_data/interbrew.db')
	print("connecting to db")
	curs=conn.cursor()
	#for row in curs.execute("SELECT * FROM TEMP ORDER BY date DESC LIMIT 1")
	for row in curs.execute("SELECT * FROM TEMP"): #ORDER BY time DESC LIMIT 1"):
		date = str(row[0])
		time = str(row[1])
		temp_c = row[2]
		temp_f = row[3]
	conn.close()
	return date, time, temp_c, temp_f
# main route
@app.route("/")
def index():
	date, time, temp_c, temp_f = getData()
	templateData = {
		'date': date,
		'time': time,
		'temp_c': temp_c,
		'temp_f': temp_f
	}
	return render_template('index.html', **templateData)
	#return flask.render_template('index.html', **templates)

if __name__ == "__main__":
   #app.run(host='0.0.0.0', debug=False)
   #app.debug=True
   app.run()
