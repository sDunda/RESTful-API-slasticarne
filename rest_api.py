#!flask/bin/python
from flask import Flask, jsonify, request, render_template, abort, make_response
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@auth.error_handler
def unauthorized():
	return make_response(jsonify({'error': 'Nemate pravo gledati kolacice.'}), 401)

slasticarne = [
	{
	'id' : 1,
	'naziv' : u'Vincek',
	'vlasnik-id': 1,
	'adresa' : u'Ilica 18',
	'gluten-free' : u'DA',
	'ocjena' : 5
	},
	{
	'id' : 2,
	'naziv' : u'The Cookie Factory',
	'vlasnik-id': 2,
	'adresa' : u'Tkalciceva 21',
	'gluten-free' : u'DA',
	'ocjena' : 5
	},
	{
	'id' : 3,
	'naziv' : u'Dulcia',
	'vlasnik-id': 3,
	'adresa' : u'Ozaljska 8',
	'gluten-free' : u'DA',
	'ocjena' : 4
	},
	{
	'id' : 4,
	'naziv' : u'Horak',
	'vlasnik-id': 4,
	'adresa' : u'Ilica 160',
	'gluten-free' : u'NE',
	'ocjena' : 4
	},
	{
	'id' : 5,
	'naziv' : u'Butik torti',
	'vlasnik-id': 4,
	'adresa' : u'Rapska ulica 38',
	'gluten-free' : u'DA',
	'ocjena' : 5
	},

	]

vlasnici = [
	{
	'vlasnik-id' : 1,
	'ime-vlasnika' : u'Stjepan Vincek',
	},
	{
	'vlasnik-id' : 2,
	'ime-vlasnika' : u'Teo Jurdan',
	},
	{
	'vlasnik-id' : 3,
	'ime-vlasnika' : u'Teuta Gluvak',
	},
	{
	'vlasnik-id' : 4,
	'ime-vlasnika' : u'Misela Jularic',
	}
	]

#popis korisnika
korisnici = {
	"loptica" : "dunda",
	"reket" : "ure01",
}

@app.route('/rznu/')
def api():
	log = open("dnevnik.txt","a")
	browser = request.user_agent.browser
	if not browser:
		log.write('/rznu/    ' + request.headers.get('User-Agent') + '\n')
	else:
		log.write('/rznu/    '+ browser + '\n')
	log.close()
	return render_template("api.html")

#autentifikacija korisnika
@auth.get_password
def get_password(username):
	if username in korisnici:
		return korisnici.get(username)
	return None

#ispis svih slasticarni

@app.route('/rznu/slasticarne', methods=['GET'])
@auth.login_required
def popis_slasticarni():
	log = open("dnevnik.txt","a")
	browser = request.user_agent.browser
	if not browser:
		log.write('/rznu/slasticarne    ' + request.headers.get('User-Agent') + '\n')
	else:
		log.write('/rznu/slasticarne    '+ browser + '\n')
	log.close()
	return jsonify({'slasticarne' : slasticarne})

#ispis svih vlasnika

@app.route('/rznu/vlasnici', methods=['GET'])
@auth.login_required
def popis_vlasnici():
	log = open("dnevnik.txt","a")
	browser = request.user_agent.browser
	if not browser:
		log.write('/rznu/vlasnici    ' + request.headers.get('User-Agent') + '\n')
	else:
		log.write('/rznu/vlasnici    '+ browser + '\n')
	log.close()
	return jsonify({'vlasnici': vlasnici})

#ugnijezdjeni ispis


@app.route('/rznu/vlasnici/<int:vlasnik_id>/slasticarne', methods=['GET'])
@auth.login_required
def popis_gnijezdo(vlasnik_id):
	log = open("dnevnik.txt","a")
	browser = request.user_agent.browser
	if not browser:
		log.write('/rznu/vlasnici/' + str(vlasnik_id) + '          '   + request.headers.get('User-Agent') + '\n')
	else:
		log.write('/rznu/vlasnici/' + str(vlasnik_id) + '                 '   + browser + '\n')
	log.close()
	vlasnik = [vlasnik for vlasnik in vlasnici if vlasnik['vlasnik-id'] == vlasnik_id]
	if not vlasnik:
		 abort(404)
	slasticarna = [slasticarna for slasticarna in slasticarne if slasticarna['vlasnik-id'] == vlasnik_id]
	return jsonify({'slasticarne': slasticarna})




#ispis slasticarni po ID

@app.route('/rznu/slasticarne/<int:slasticarna_id>', methods=['GET'])
@auth.login_required
def slasticarna(slasticarna_id):
	log = open("dnevnik.txt","a")
	browser = request.user_agent.browser
	if not browser:
		log.write('/rznu/slasticarne/' + str(slasticarna_id) + '         '   + request.headers.get('User-Agent') + '\n')
	else:
		log.write('/rznu/slasticarne/' + str(slasticarna_id) + '          '  + browser + '\n')
	log.close()
	slasticarna = [slasticarna for slasticarna in slasticarne if slasticarna['id'] == slasticarna_id]
	if not slasticarna:
		abort(404)
	return jsonify({'slasticarne': slasticarna})

#ispis vlasnika po ID

@app.route('/rznu/vlasnici/<int:vlasnik_id>', methods=['GET'])
@auth.login_required
def vlasnik(vlasnik_id):
	log = open("dnevnik.txt","a")
	browser = request.user_agent.browser
	if not browser:
		log.write('/rznu/vlasnici/' +  str(vlasnik_id) + '        '  + request.headers.get('User-Agent') + '\n')
	else:
		log.write('/rznu/vlasnici/' + str(vlasnik_id) +   '           '  + browser + '\n')
	log.close()
	vlasnik = [vlasnik for vlasnik in vlasnici if vlasnik['vlasnik-id'] == vlasnik_id]
	if not vlasnik:
		abort(404)
	return jsonify({'vlasnici': vlasnik})

#brisanje slasticarne po ID

@app.route('/rznu/slasticarne/<int:slasticarna_id>', methods=['DELETE'])
@auth.login_required
def brisanje_slasticarne(slasticarna_id):
	log = open("dnevnik.txt","a")
	browser = request.user_agent.browser
	if not browser:
		log.write('/rznu/slasticarne/' + str(slasticarna_id)  + '     ' +  request.headers.get('User-Agent') + '\n')
	else:
		log.write('/rznu/slasticarne/' + str(slasticarna_id) + '         '  +   browser + '\n')
	log.close()
	slasticarna = [slasticarna for slasticarna in slasticarne if slasticarna['id'] == slasticarna_id]
	if not slasticarna:
		abort(404)
	slasticarne.remove(slasticarna[0])
	return jsonify({'result': True})

#brisanje vlasnika po ID

@app.route('/rznu/vlasnici/<int:vlasnik_id>', methods=['DELETE'])
@auth.login_required
def brisanje_vlasnika(vlasnik_id):
	log = open("dnevnik.txt","a")
	browser = request.user_agent.browser
	if not browser:
		log.write('/rznu/vlasnici/' + str(vlasnik_id) + '           '  +  request.headers.get('User-Agent') + '\n')
	else:
		log.write('/rznu/vlasnici/' + str(vlasnik_id) + '             ' +  browser + '\n')
	log.close()
	vlasnik = [vlasnik for vlasnik in vlasnici if vlasnik['vlasnik-id'] == vlasnik_id]
	if not vlasnik:
		abort(404)
	vlasnici.remove(vlasnik[0])
	return jsonify({'result': True})

#dodavanje nove slasticarne

@app.route('/rznu/slasticarne', methods=['POST'])
@auth.login_required
def nova_slasticarna():
	log = open("dnevnik.txt","a")
	browser = request.user_agent.browser
	if not browser:
		log.write('/rznu/slasticarne    ' + request.headers.get('User-Agent') + '\n')
	else:
		log.write('/rznu/slasticarne    '+ browser + '\n')
	log.close()
	if not request.json or not 'naziv' in request.json or not 'adresa' in request.json or not 'vlasnik-id' in request.json:
		abort(400)
	slasticarna = {
	'id': slasticarne[-1]['id']+1,
	'naziv': request.json['naziv'],
	'vlasnik-id': request.json['vlasnik-id'],
	'adresa': request.json['adresa'],
	'gluten-free' : request.json.get('gluten-free',"-"),
	'ocjena' : request.json.get('ocjena',"-")
	}
	slasticarne.append(slasticarna)
	return jsonify({'slasticarna' : slasticarna }), 201

#dodavanje novog vlasnika

@app.route('/rznu/vlasnici', methods=['POST'])
@auth.login_required
def novi_vlasnik():
	log = open("dnevnik.txt","a")
	browser = request.user_agent.browser
	if not browser:
		log.write('/rznu/vlasnici    ' + request.headers.get('User-Agent') + '\n')
	else:
		log.write('/rznu/vlasnici    '+ browser + '\n')
	log.close()
	if not request.json or not 'vlasnik-id' in request.json or not 'ime-vlasnika' in request.json:
		abort(400)
	vlasnik = {
	'vlasnik-id': request.json['vlasnik-id'],
	'ime-vlasnika': request.json['ime-vlasnika']
	}
	vlasnici.append(vlasnik)
	return jsonify({'vlasnici' : vlasnik }), 201

#updatanje slasticarne

@app.route('/rznu/slasticarne/<int:slasticarna_id>', methods=['PUT'])
@auth.login_required
def update_slasticarna(slasticarna_id):
	log = open("dnevnik.txt","a")
	browser = request.user_agent.browser
	if not browser:
		log.write('/rznu/slasticarne/' + str(slasticarna_id) + '         ' + request.headers.get('User-Agent') + '\n')
	else:
		log.write('/rznu/slasticarne/' + str(slasticarna_id) + '         '   + browser + '\n')
	log.close()
	slasticarna = [slasticarna for slasticarna in slasticarne if slasticarna['id'] == slasticarna_id]
	if not slasticarna or not request.json:
		abort(400)
	slasticarna[0]['naziv'] = request.json.get('naziv', slasticarna[0]['naziv'])
	slasticarna[0]['vlasnik-id'] = request.json.get('vlasnik-id', slasticarna[0]['vlasnik-id'])
	slasticarna[0]['adresa'] = request.json.get('adresa', slasticarna[0]['adresa'])
	slasticarna[0]['gluten-free'] = request.json.get('gluten-free', slasticarna[0]['gluten-free'])
	slasticarna[0]['ocjena'] = request.json.get('ocjena', slasticarna[0]['ocjena'])
	slasticarna[0]['id'] = request.json.get('id', slasticarna[0]['id'])

	return jsonify({'slasticarna': slasticarna[0]})

#updatanje vlasnika

@app.route('/rznu/vlasnici/<int:vlasnik_id>', methods=['PUT'])
@auth.login_required
def update_vlasnik(vlasnik_id):
	log = open("dnevnik.txt","a")
	browser = request.user_agent.browser
	if not browser:
		log.write('/rznu/vlasnici/' + str(vlasnik_id)  + '         '  + request.headers.get('User-Agent') + '\n')
	else:
		log.write('/rznu/vlasnici/' + str(vlasnik_id)  + '         '    + browser + '\n')
	log.close()
	vlasnik = [vlasnik for vlasnik in vlasnici if vlasnik['vlasnik-id'] == vlasnik_id]
	if not vlasnik or not request.json:
		abort(400)
	vlasnik[0]['vlasnik-id'] = request.json.get('vlasnik-id', vlasnik[0]['vlasnik-id'])
	vlasnik[0]['ime-vlasnika'] = request.json.get('ime-vlasnika', vlasnik[0]['ime-vlasnika'])

	return jsonify({'vlasnik': vlasnik[0]})


if __name__ == '__main__':
	app.run(debug=True)
