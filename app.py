from flask import Flask, Response, request
from datetime import datetime
import json
import requests

app = Flask(__name__)


@app.route('/')
def homepage():
	the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")
	
	return """
		<h1>Hello heroku</h1>
		<p>It is currently {time}.</p>
		
		<img src="http://loremflickr.com/600/400" />
	""".format(time=the_time)


@app.route('/DialogFlow/Test', methods=['POST'])
def post_dialogflow_test():
	print("Got request for DialogFlow!")
	x=json.loads(request.data.decode('utf-8'))
	print(x["queryResult"]["fulfillmentMessages"])
	testdata={"query": "{getAccounts(filter:{filterParams :[{property: accountNumber operation:EQUALS value: '6514363164383'}]},pagination: { offset: 0 , limit : 10}){accounts {accountNumber customer{name}}}}"}
	r=requests.post('https://hyperlite-graphql-server-release.pcfomactl.dev.intranet/graphql', data = testdata)
	print(r.json())
	resp_obj = {
		"payload": {
			"google": {
				"expectUserResponse": True,
				"richResponse": {
					"items": [
						{
							"simpleResponse": {
								"textToSpeech": "This is a speech. Temperature of Blr is 0C"
							}
						}
					]
				}
			}
		}
	}
	resp = Response(json.dumps(resp_obj).encode('utf-8'), status=200, mimetype='application/json')
	resp.headers['Access-Control-Allow-Origin'] = '*'
	resp.headers['Content-Type'] = 'application/json'
	return resp


if __name__ == '__main__':
	app.run(debug=True, use_reloader=True)
