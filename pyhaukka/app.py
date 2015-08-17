# Define the Flask WSGI application object
from flask import send_from_directory
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask('pyhaukka', static_url_path='', static_folder='../haukka-ui')

# Configuration
app.config.from_object('config')

# DB Module
db = SQLAlchemy(app)

# WhiteNoise to smartly serve static files (support gzip, caching and other stuff suitable for using behind a CDN )!
#from whitenoise import WhiteNoise
#app.wsgi_app = WhiteNoise(app.wsgi_app,
#                          root=app.config['STATIC_DIR'],
#                          prefix=app.config.get('STATIC_PREFIX', ''))

# Sample HTTP error handling
# @app.errorhandler(404)
# def not_found(error):
#    return render_template('404.html'), 404

@app.route('/')
def send_home():
    return app.send_static_file('index.html')

@app.route('/bower_components/<path:path>')
def send_bower(path):
  return send_from_directory(app.config.get('BASE_DIR') + '/bower_components', path)

# Flask-RESTful
from flask_restful import Api
api = Api(app)

from pyhaukka.resources.trials import Trials, TrialResource

# Register endpoint(s)
api.add_resource(Trials,  '/trials')
api.add_resource(TrialResource,  '/trials/<string:trial_id>')

app.logger.info('Initialized web app!')