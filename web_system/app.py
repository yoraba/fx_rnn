# coding: utf-8
import binascii, os, sys
import numpy as np
from flask import Flask, render_template, make_response, session, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from sample_model import SampleModel
from models.login_model import LoginModel, UserContext
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from back_system.api.quandl_api import QuandlAPI
from back_system.api.ta_api import TAlib_API
from back_system.api.keras_api import KerasAPI


app = Flask(__name__)
app.secret_key = binascii.hexlify(os.urandom(24))
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return UserContext(user_id)


@app.route('/')
def login():
    if 'login' in session and session['login']:
        return redirect('/top')
    else:
        return render_template('login.html')


@app.route('/', methods=['POST'])
def on_login():
    session['password'] = request.form['password']
    if not LoginModel().on_login(session['password']):
        session.pop('password', None)
        if 'login' in session:
            session['login'] = False
            logout_user()
    else:
        session['login'] = True
        login_user(UserContext('admin'))
    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    session.pop('password', None)
    session['login'] = False
    logout_user()
    return redirect('/')


@app.route('/top', methods=['GET', 'POST'])
@login_required
def menu():
    return render_template('top.html')


@app.route('/quandl', methods=['GET', 'POST'])
@login_required
def quandl():
    context = LoginModel().get_context(session['password'])
    api = QuandlAPI(context)
    data = api.get_indicative_history_dict()
    return render_template('quandl.html', data=data)


@app.route('/quandl/gethistory')
@login_required
def quandl_gethistory():
    context = LoginModel().get_context(session['password'])
    api = QuandlAPI(context)
    api.set_indicative_history()
    data = api.get_indicative_history_dict()
    return render_template('quandl.html', data=data)


@app.route('/talib', methods=['GET', 'POST'])
@login_required
def talib():
    context = LoginModel().get_context(session['password'])
    answer = TAlib_API(context).get_technicals()
    return render_template('talib.html', data=answer, columnCount=np.shape(answer)[1])


@app.route('/prediction', methods=['GET', 'POST'])
@login_required
def prediction():
    return render_template('prediction.html')


@app.route('/prediction/predict', methods=['GET', 'POST'])
@login_required
def prediction_predict():
    context = LoginModel().get_context(session['password'])
    api = KerasAPI(context)
    hl_score = api.predict()
    return render_template('prediction.html', hl_score=enumerate(hl_score))


@app.route('/sampleplot')
def sample_plot():
    data = SampleModel().get_dummy_graph()
    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Length'] = len(data)
    return response


if __name__ == "__main__":
    app.run(threaded=False)


