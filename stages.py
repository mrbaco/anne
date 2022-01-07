
def init(request, response, session):
    response['response']['text'] = request.json.get("request", {}).get("command", "") + " - init"
    session['stage'] = 1

def dateTimeClarification(request, response, session):
    response['response']['text'] = request.json.get("request", {}).get("command", "") + " - dateTimeClarification"
    session['stage'] = 2

def successResult(request, response, session):
    response['response']['text'] = request.json.get("request", {}).get("command", "") + " - successResult"
    response['response']['end_session'] = True


class Stages:
    stages = [
        {   
            "auth_required": False,
            "method": init
        },
        {
            "auth_required": False,
            "method": dateTimeClarification
        },
        {
            "auth_required": True,
            "method": successResult
        },
    ]
