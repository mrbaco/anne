
from flask import Flask, request
import json

from auth import Auth
from stages import Stages

app = Flask(__name__)

@app.route("/", methods=["POST"])
def main():
    session_state = request.json.get("state", {}).get("session", {})
    command = request.json.get("request", {}).get("command", "")

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        },
        "session_state": {}
    }

    stage = abs(session_state['stage']) if "stage" in session_state else 0
    stage = stage if stage <= len(Stages.stages) else 0

    if Stages.stages[stage]['auth_required']:
        if not "authed" in session_state:
            if not "code_phrase" in session_state:
                session_state['code_phrase'] = Auth.create_code_phrase()
                response['response']['text'] = (
                    "Записала. Нужно подтверждение. Вопрос: %s" %
                        session_state['code_phrase']
                )
            else:
                if Auth.check(session_state['code_phrase'], command):
                    session_state['authed'] = True
                else:
                    session_state['code_phrase'] = Auth.create_code_phrase()
                    response['response']['text'] = (
                        "Неправильный ответ. Попробуем ещё раз. Вопрос: %s" %
                            session_state['code_phrase']
                    )

    if not Stages.stages[stage]['auth_required'] or session_state['authed']:
        Stages.stages[stage]['method'](request, response)

    response['session_state'] = {**session_state, **response['session_state']}

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


if __name__ == "__main__":
    app.run()
