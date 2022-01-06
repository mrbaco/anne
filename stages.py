
def init(request, response):
    response['response']['text'] = request.json.get("request", {}).get("command", "") + " - init"
    response['response']['state']['session']['stage'] = 1

def dateTimeClarification(request, response):
    response['response']['text'] = request.json.get("request", {}).get("command", "") + " - dateTimeClarification"
    response['response']['state']['session']['stage'] = 2

def successResult(request, response):
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
