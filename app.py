import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)).replace('\\', '/'))
sys.path.append(parent_dir)
from flask import Flask, render_template, request, Response
app = Flask(__name__)
import json


@app.route('/DialogFlow/Test', methods=['POST'])
def post_dialogflow_test():
	print("Got request for DialogFlow!")
	resp_obj = {
		'speech': 'This is a speech. Temperature of Blr is 0C',
		'displayText': 'This is a speech. Temperature of Blr is 0C',
		'source': 'Temp API'
	}
	resp = Response(json.dumps(resp_obj).encode('utf-8'), status=200, mimetype='application/json')
	resp.headers['Access-Control-Allow-Origin'] = '*'
	resp.headers['Content-Type'] = 'application/json'
	return resp


def start_server():
	app.run()


if __name__ == "__main__":
	start_server()
