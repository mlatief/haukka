# Import flask and template operators
from flask import Flask, g
from flask_restful import Api

from pyhaukka.db import ClinicalTrialsDatabase

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Flask-RESTful
api = Api(app)

# DB Module
#db = ClinicalTrialsDatabase()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = ClinicalTrialsDatabase(app.config.get('DATABASE_URI',''))
    return db


@app.teardown_appcontext
def close_connection(exception):
    print "App context tearDown called..."
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Sample HTTP error handling
#@app.errorhandler(404)
#def not_found(error):
#    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from pyhaukka.resources.trials import  Trials
from pyhaukka.resources.trial import  Trial

# Register endpoint(s)
api.add_resource(Trials, '/1/trials')
api.add_resource(Trial,  '/1/trials/<string:trial_id>')