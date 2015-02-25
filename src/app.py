# -*- coding: utf-8 -*-

from flask import Flask
app = Flask(__name__)

from flask import render_template


@app.route('/')
def index(name=None):
    return render_template('index.html')


@app.route('/autocomplete', methods=['POST'])
def autocomplete(name=None):
    return None


if __name__ == '__main__':
    app.run()
