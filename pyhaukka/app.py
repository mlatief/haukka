# Define the Flask WSGI application object
from flask import Flask, g
app = Flask('pyhaukka')

# Configuration
app.config.from_object('config')

# WhiteNoise to smartly serve static files (support gzip, caching and other stuff suitable for using behind a CDN )!
from whitenoise import WhiteNoise
app.wsgi_app = WhiteNoise(app.wsgi_app,
                          root=app.config.get('STATIC_DIR', app.config['BASE_DIR'] + '/static'),
                          prefix=app.config.get('STATIC_PREFIX', ''))

# DB Module
from pyhaukka.db import ClinicalTrialsDatabase
db = ClinicalTrialsDatabase()


def get_db():
    gdb = getattr(g, '_database', None)
    if gdb is None:
        gdb = g._database = ClinicalTrialsDatabase(app.config.get('DATABASE_URI', ''))
    return gdb


@app.teardown_appcontext
def close_connection(exception):
    print "App context tearDown called..."
    gdb = getattr(g, '_database', None)
    if gdb is not None:
        gdb.close()

# Sample HTTP error handling
# @app.errorhandler(404)
# def not_found(error):
#    return render_template('404.html'), 404

# Flask-RESTful
from flask_restful import Api
api = Api(app)

# Import a module / component using its blueprint handler variable (mod_auth)
from pyhaukka.resources.trials import Trials
from pyhaukka.resources.trial import Trial

# Register endpoint(s)
api.add_resource(Trials, '/trials')
api.add_resource(Trial,  '/trials/<string:trial_id>')
