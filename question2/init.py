from flask import Flask, render_template, json, request, jsonify, flash, redirect
from flask.views import MethodView


import happybase
from application import services

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    HBASE_HOST = 'localhost',
    HBASE_PORT = 9090,
    SECRET_KEY = 'LIWJFJWLEIFJLWEKFJLDSIFWKWEJHF9283LKWEJF'
))

@app.route('/')
def main():
    return render_template('index.html')


@app.route('/api/data')
def get_data():
    service = services.HBaseService();
    return jsonify(service.retrieve_data())


@app.route('/import', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        if file:
            service = services.DataService()
            service.import_from_file(file)
            flash('Data import succeeded')
        else:
            flash('No file selected')
    except Exception as ex:
        flash('Error during import')
    return redirect('/')

if __name__ == "__main__":
    app.run()
