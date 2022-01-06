
class Stages:
    @staticmethod
    def init(request, response):
        response['response']['text'] = request.json['command']

    @staticmethod
    def dateTimeClarification(request, response):
        response['response']['text'] = request.json['command']

    @staticmethod
    def successResult(request, response):
        response['response']['text'] = request.json['command']
        response['response']['end_session'] = True

    order = [
        init,
        dateTimeClarification,
        successResult,
    ]

    authRequired = [
        successResult
    ]
