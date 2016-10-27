import urllib3
import json
import config



#	transl["KEY_STOP"]="Player.Stop" {"jsonrpc":"2.0", "method":"Player.GetProperties", "params":{ "playerid":1, "properties":["time","speed","totaltime", "percentage"]},"id":1}


def kodiJsonCall(jsonDATA):
	http = urllib3.PoolManager()
	encoded_data = json.dumps(jsonDATA)
	req = http.request(method='POST', url=JSONRPC_URL, headers={'Content-Type': 'application/json'}, body = encoded_data)
	JREQ = json.loads(req.data.decode('utf-8'))
	return JREQ


def kodiSendKey(eventName):
	transl=dict()
	transl["KEY_LEFT"]	= {"jsonrpc":"2.0", "method":"Input.Left", "id":1}
	transl["KEY_RIGHT"]	= {"jsonrpc":"2.0", "method":"Input.Right", "id":1}
	transl["KEY_UP"]	= {"jsonrpc":"2.0", "method":"Input.Up", "id":1}
	transl["KEY_DN"]	= {"jsonrpc":"2.0", "method":"Input.Down", "id":1}
	transl["KEY_ENTER"]	= {"jsonrpc":"2.0", "method":"Input.Select", "id":1}
	transl["KEY_ESCAPE"]	= {"jsonrpc":"2.0", "method":"Input.Back", "id":1}
	transl["KEY_PLAY"]	= {"jsonrpc":"2.0", "method":"Player.PlayPause", "params":{ "playerid":1 },"id":1}
	transl["KEY_STOP"]	= {"jsonrpc":"2.0", "method":"Player.Stop", "params":{ "playerid":1 },"id":1}

	if eventName in transl:
		jsonDATA =  transl[eventName]
		kodiJsonCall(jsonDATA)

