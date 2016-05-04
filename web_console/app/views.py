from flask import render_template, request, jsonify
from app import app, models

@app.route("/", methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('main.html')


@app.route("/reflash", methods=['GET'])
def reflash():
    if request.method =='GET':
        data = models.monitor.query.filter_by(id='1').first()
        data_dict = vars(data)
        data_dict.pop('_sa_instance_state')
        return jsonify(data_dict)
