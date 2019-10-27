# coding: utf-8
from flask import Flask, render_template, make_response
from sample_model import SampleModel
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bs = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sampleplot')
def sample_plot():
    data = SampleModel().get_dummy_graph()
    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Length'] = len(data)
    return response


if __name__ == "__main__":
    app.run()


