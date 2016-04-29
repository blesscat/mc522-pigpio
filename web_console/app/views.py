import __builtin__

from flask import render_template, request, jsonify
from app import app, models

__builtin__.data = {'addr': 'None',
                    'lcd' : '0',
                    'dice': '0 0 0 0 0 0',
                    'attr': 'None'}


s = models.data_pipe()
s.setDaemon(True)
s.start()


@app.route("/", methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('main.html', data=__builtin__.data)


@app.route("/reflash", methods=['GET'])
def reflask():
    if request.method == 'GET':
        if type(__builtin__.data['dice']) is str and '=' not in __builtin__.data['dice']:
            dice = __builtin__.data['dice'].split(' ')
            sum = 0
            for i in dice:
                sum = sum + int(i)
            __builtin__.data['dice'] = __builtin__.data['dice'] + ' = ' + str(sum)

        if type(__builtin__.data['attr']) is str:
            __builtin__.data['attr'] = __builtin__.data['attr'].split(' ')

        return jsonify(__builtin__.data)
