
import datetime
from auth import Auth

def getDatetimeEntity(request):
    datetime_entities = list(filter(
        lambda entity: entity['type'] == "YANDEX.DATETIME",
        request['request']['nlu']['entities']
    ))

    if len(datetime_entities) != 1:
        return None
    
    return dict(datetime_entities[0]).get("value", None)

def init(request, response, session):
    # Проверить наличие даты в request.nlu.entities
    datetime_entity = getDatetimeEntity(request.json)
    session['datetime'] = datetime_entity

    # Если даты нет - вызываем dateTimeClarification
    if datetime_entity == None:
        dateTimeClarification(request, response, session)
        return
    
    # Если дата есть - вызываем approveTime и осуществляем переход на этап 1
    session['stage'] = 1

    approveTime(request, response, session)

def dateTimeClarification(request, response, session):
    # Запрашиваем дату и время
    response['response']['text'] = "На какое время делать заявку?"
    session['stage'] = 1

def approveTime(request, response, session):
    # Проверяем корректность заполнения даты и времени
    session['datetime'] = (getDatetimeEntity(request.json) if "datetime_entity" 
        in session and session['datetime_entity'] == None
            else session['datetime'])
    
    if session['datetime'] == None:
        response['response']['text'] = ("Не смогла определить дату и время " + 
            "для создания заявки. Пожалуйста, повторите.")
        session['datetime_entity'] = None

        return
    
    order_datetime = dict(session['datetime'])

    if order_datetime.get("day", None) == None:
        response['response']['text'] = ("Не смогла определить дату " + 
            "для создания заявки. Пожалуйста, повторите.")
        session['datetime_entity'] = None
        
        return
    
    if order_datetime.get("hour", None) == None:
        response['response']['text'] = ("Не смогла определить время " + 
            "для создания заявки. Пожалуйста, повторите.")
        session['datetime_entity'] = None
        
        return

    if order_datetime.get("day", 0) < 1:
        response['response']['text'] = ("Нельзя отправить заказ в прошлое. " +
            "Пожалуйста, повторите.")
        session['datetime_entity'] = None
        
        return
    
    # Осуществляем расчёт времени по относительным и абсолютным величинам
    current_datetime = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    
    if "day_is_relative" in order_datetime and "day" in order_datetime:
        if order_datetime['day_is_relative']:
            current_datetime += datetime.timedelta(days=order_datetime['day'])
        else:
            current_datetime.replace(day=order_datetime['day'])

    if "hour_is_relative" in order_datetime and "hour" in order_datetime:
        if order_datetime['hour_is_relative']:
            current_datetime += datetime.timedelta(hours=order_datetime['hour'])
        else:
            current_datetime.replace(hour=order_datetime['hour'])
    
    # Сохраняем расчитанную дату и переходим на следующий этап
    session['datetime'] = current_datetime
    session['stage'] = 2

    successResult(request, response, session)

def successResult(request, response, session):
    if not "code_phrase" in session:
        session['code_phrase'] = Auth.create_code_phrase()
        response['response']['text'] = (
            "Записала. Нужно подтверждение. Вопрос: %s" %
                session['code_phrase']
        )
    else:
        if Auth.check(session['code_phrase'], session['last_command']):
            # TODO: выполняем действие
            response['response']['text'] = "Сформировала заявку на доставку. На почту придёт подтверждение. %s" % session['datetime']
            response['response']['end_session'] = True
        else:
            session['code_phrase'] = Auth.create_code_phrase()
            response['response']['text'] = (
                "Неправильный ответ. Попробуем ещё раз. Вопрос: %s" %
                    session['code_phrase']
            )


class Stages:
    stages = [
        init,
        approveTime,
        successResult,
    ]
