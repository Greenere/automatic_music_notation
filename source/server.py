"""
A simple server designed to cast a "virtual printer"
- Serve the index page
- Serve the requested data
"""

import json
from flask import Flask, request, jsonify, send_file
from gevent.pywsgi import WSGIServer
from gevent import monkey

from exchange import read_message, leave_message

app = Flask(__name__)

@app.route('/')
def index():
    filename='index.html'
    return send_file(filename)

@app.route('/audio/<path>')
def audio(path):
    filepath = "./results/%s"%(path)
    try: 
        with open(filepath, "rb") as f:
            data = f.read()
        return data
    except:
        return ''

@app.route('/data',methods=['GET'])
def dataServe():
    reqs=request.args.get('request')
    reqs = json.loads(reqs)
    if reqs['type'] == 'notation':
        melody = read_message("melody")
        if melody == "":
            return ""
        resp = None
        with open("./%s.svg"%(melody), "r") as f:
            resp = f.read()
        return resp
    elif reqs['type'] == 'recording':
        recording = read_message("recording")
        if recording == "":
            return ""
        resp = None
        with open("./%s.svg"%(recording), "r") as f:
            resp = f.read()
        return resp
    elif reqs['type'] == 'audio':
        recorded = read_message("audio")
        if recorded == "":
            return jsonify({"name":""})
        return jsonify({"name":"%s.wav"%(str(recorded))})
    elif reqs['type'] == 'ping':
        updated = read_message("update")
        if updated == 1:
            return jsonify({"update":1})
        elif updated == 2:
            leave_message("update", -1)
            return jsonify({"update":2})
        else:
            return jsonify({"update":-1})
    return ""

if __name__ == '__main__':
    monkey.patch_all()

    host: str = '10.49.53.185'
    port: int = 8880

    print('SERVING ON: ', 'http://' + host + ':' + str(port))

    http_server = WSGIServer((host, port), app)
    http_server.serve_forever()