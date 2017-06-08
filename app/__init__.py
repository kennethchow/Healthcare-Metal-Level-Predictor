import logging
from sklearn.externals import joblib

from flask import Flask

# create logger for app
logger = logging.getLogger('app')
logger.setLevel(logging.INFO)

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)

app = Flask(__name__)
app.config.from_object("app.config")

# unpickle my model
estimator = joblib.load('models/HealthInsuranceLogRFinal5.pkl')
target_names = {'Bronze':'Bronze', 'Silver':'Silver', 'Gold':'Gold', 'Platinum':'Platinum'}


from .views import *   # flake8: noqa


# Handle Bad Requests
@app.errorhandler(404)
def page_not_found(e):
    """Page Not Found"""
    return render_template('404.html'), 404
