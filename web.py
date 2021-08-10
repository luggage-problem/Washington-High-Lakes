
from flask import Flask, jsonify, request, abort
import sqlite3

app = Flask(__name__)

@app.route('/api/lakes/')
def lake_index():
	with sqlite3.connect('highlakes.db') as con:
		db = con.cursor()

		# possible query params
		name = request.args.get('name')
		overabundant = request.args.get('overabundant')
		county = request.args.get('county')

		query = "SELECT id, name FROM lakes WHERE 1"
		params = []
		if overabundant:
			query += " AND overabundant = ?"
			params.append(overabundant)
		if name:
			query += " AND name LIKE ?"
			params.append('%' + name + '%')
		if county:
			query += " AND county = ?"
			params.append(county)

		results = db.execute(query, params).fetchall()
		return jsonify({'results' : [{'id' : lake[0], 'name' : lake[1]} for lake in results]})

@app.route('/api/lakes/<lake_id>')
def lakes(lake_id):
	with sqlite3.connect('highlakes.db') as con:
		db = con.cursor()
		result = db.execute("SELECT * FROM lakes WHERE id=?", (lake_id,)).fetchall()
		fishes = db.execute("SELECT fishes.species FROM fishes INNER JOIN fish_lake ON fish_lake.fishID = fishes.id WHERE fish_lake.lakeID = ?", (lake_id,)).fetchall()
		if not result:
			abort(404)
		return jsonify({
			'id' : result[0][0],
			'name' : result[0][1],
			'county' : result[0][2],
			'area' : result[0][3],
			'elevation' : result[0][4],
			'TRS' : result[0][5],
			'latitude' : result[0][6],
			'longitude' : result[0][7],
			'overabundant' : result[0][8],
			'fish_species': [f[0] for f in fishes]
		})

# enable CORS (for now)
@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
	app.run(debug=True)