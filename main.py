
from flask import Flask, request
import json

from stages import Stages

app = Flask(__name__)

sessions_storage = {}

@app.route("/", methods=["POST"])
def main():
    application_id = request.json['session']['application']['application_id']

    session = sessions_storage.get(application_id, {})
    session['last_command'] = request.json.get("request", {}).get("command", "")

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    stage = abs(session['stage']) if "stage" in session else 0
    stage = stage if stage <= len(Stages.stages) else 0

    Stages.stages[stage](request, response, session)

    if response['response']['end_session']:
        sessions_storage.pop(application_id, None)
    else:
        sessions_storage[application_id] = session

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


if __name__ == "__main__":
    app.run()
