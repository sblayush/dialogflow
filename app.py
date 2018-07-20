from flask import Flask, Response, request
from datetime import datetime
import json
import requests

app = Flask(__name__)

accountMap={"123456789":"vivek tiwari","223456789":"Madhu Bhangi","323456789":"Hari Krishnan"}
sessMap={}
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
	print(x)
	print("x[\"session\"]=",x["session"])
	sessionId=x["session"]
	sessionId=sessionId[sessionId.find("projects/myfirst-6a1d1/agent/sessions/")+len("projects/myfirst-6a1d1/agent/sessions/"):]

	#testdata={"query": "{getAccounts(filter:{filterParams :[{property: accountNumber operation:EQUALS value: '6514363164383'}]},pagination: { offset: 0 , limit : 10}){accounts {accountNumber customer{name}}}}"}
	#r=requests.post('https://hyperlite-graphql-server-release.pcfomactl.dev.intranet/graphql', data = testdata,verify=False)
	#print(r.json())
	respString=""
	if x["queryResult"]["intent"]["displayName"]=="getAccountInfo":
		if x["queryResult"]["parameters"] is not None and x["queryResult"]["parameters"]["acc_no"] is not None:
			if x["queryResult"]["parameters"]["acc_no"] in accountMap:
				respString="Thanks for providing me the account Number {}.Your customer name is {}.".format(x["queryResult"]["parameters"]["acc_no"],accountMap[x["queryResult"]["parameters"]["acc_no"]])
				sessMap[sessionId]=True
				print(sessMap)
			else:
				respString="Your account number {} seems to be wrong or not registered.Please provide correct Account Number.".format(x["queryResult"]["parameters"]["acc_no"])
		else:
			respString="Your account number {} seems to be wrong.Please provide correct Account Number."
	elif x["queryResult"]["intent"]["displayName"]=="temperature intent":
		respString="Temperature of Blr is 20 degrees Celcius!"
	elif x["queryResult"]["intent"]["displayName"]=="internet-outage":
		if sessionId not in sessMap:
			respString="Please provide me your account Number"
		else:
			respString="There seems to be a network issue going on"
	elif x["queryResult"]["intent"]["displayName"]=="getBillingInfo":
		if sessionId not in sessMap:
			respString="Please provide me your account Number"
		else:
			respString="Your account balance is $1000"
	else:
		respString="Intent identified {} has not been mapped to any specific backend.This is a generic response".format(x["queryResult"]["intent"]["displayName"])


	resp_obj = {
		"payload": {
			"google": {
				"expectUserResponse": True,
				"richResponse": {
					"items": [
						{
							"simpleResponse": {
								"textToSpeech": respString
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
