import json
from flask import Flask, request, send_file

from exchange import read_message

app = Flask(__name__)

@app.route('/')
def index():
    filename='index.html'
    return send_file(filename)

@app.route('/data',methods=['GET'])
def dataServe():
    reqs=request.args.get('request')
    reqs = json.loads(reqs)
    if reqs['type'] == 'notation':
        melody = read_message("melody")
        if melody == "":
            return ""
        resp = None
        with open("../%s.svg"%(melody), "r") as f:
            resp = f.read()
        return resp
    elif reqs['type'] == 'recording':
        recording = read_message("recording")
        if recording == "":
            return ""
        resp = None
        with open("../%s.svg"%(recording), "r") as f:
            resp = f.read()
        return resp
    elif reqs['type'] == 'email':
        email_address = reqs['address']
        print(email_address)
        return ""
    return ""


from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()

if __name__ == '__main__':
    host: str = '10.49.53.185'
    port: int = 8880

    print('SERVING ON: ', 'http://' + host + ':' + str(port))

    http_server = WSGIServer((host, port), app)
    http_server.serve_forever()