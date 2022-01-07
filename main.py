
from flask import Flask, request
import json

from auth import Auth
from stages import Stages

app = Flask(__name__)

sessions_storage = {}

@app.route("/", methods=["POST"])
def main():
    application_id = request.json['session']['application']['application_id']
    command = request.json.get("request", {}).get("command", "")

    session = sessions_storage.get(application_id, {})

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    stage = abs(session['stage']) if "stage" in session else 0
    stage = stage if stage <= len(Stages.stages) else 0

    if Stages.stages[stage]['auth_required']:
        if not "authed" in session:
            if not "code_phrase" in session:
                session['code_phrase'] = Auth.create_code_phrase()
                response['response']['text'] = (
                    "Записала. Нужно подтверждение. Вопрос: %s" %
                        session['code_phrase']
                )
            else:
                if Auth.check(session['code_phrase'], command):
                    session['authed'] = True
                else:
                    session['code_phrase'] = Auth.create_code_phrase()
                    response['response']['text'] = (
                        "Неправильный ответ. Попробуем ещё раз. Вопрос: %s" %
                            session['code_phrase']
                    )

    if not Stages.stages[stage]['auth_required'] or session['authed']:
        Stages.stages[stage]['method'](request, response, session)

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
