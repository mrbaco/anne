
def init(request, response):
    response['response']['text'] = request.json['command']

def dateTimeClarification(request, response):
    response['response']['text'] = request.json['command']

def successResult(request, response):
    response['response']['text'] = request.json['command']
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
