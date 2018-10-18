import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import datetime
import json

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

ASK_APPLICATION_ID = 'amzn1.ask.skill.032dbe18-8f0f-4620-b594-94a20853c97c'
ASK_VERIFY_REQUESTS = True
ASK_VERIFY_TIMESTAMP_DEBUG = True


@ask.intent("inspire_me")
def main_function():
    return dinner_recommendation()

    
@ask.intent("AMAZON.StopIntent")
def stop_function():
    return statement("See you tomorrow")

    
@ask.intent("AMAZON.CancelIntent")
def cancel_function():
    return statement("See you tomorrow")


@ask.launch
def launched():
    return dinner_recommendation()

@ask.session_ended
def session_ended():
    return "{}", 200

# --------------- Main handler ------------------
def lambda_handler(event, context):
    if event['session']['application']['applicationId'] != "amzn1.ask.skill.032dbe18-8f0f-4620-b594-94a20853c97c":
        print("wrong app id")
        return ''
    print("event.session.application.applicationId=" +
          str(event['session']['application']['applicationId']))
    if event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])


# --------------- Response handler ------------------
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    jj = {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
    return app.response_class(json.dumps(jj), content_type='application/json')


# --------------- Events ------------------
def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    if intent_name == "inspire_me":
        return dinner_recommendation()


#--------------- App Functions ------------------------
def dinner_recommendation():
    session_attributes = {}
    card_title = "Daily inspiration"
    dinner = get_dinner()
    speech_output = "Here we go. "+dinner
    reprompt_text = dinner
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_dinner():
    now = datetime.datetime.now()
    day = now.day
    return food_list[int(day)%10]


#---------------- Food List ----------------------------
#BURAYA_YENI_STRINGLER
food_list = ("You are the nicest thing on earth that can stand on its own feet!", "You are the nicest thing on earth that can stand on its own feet!", "You shine bright like a diamond today", "You shine bright like a diamond today", "You are the nicest thing on earth that can stand on its own feet!", "You shine bright like a diamond today", "You are the nicest thing on earth that can stand on its own feet!", "You shine bright like a diamond today", "You are the nicest thing on earth that can stand on its own feet!", "You shine bright like a diamond today", "You are the nicest thing on earth that can stand on its own feet!", "You shine bright like a diamond today")


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.config['ASK_APPLICATION_ID'] = 'amzn1.ask.skill.032dbe18-8f0f-4620-b594-94a20853c97c'
    app.config['ASK_VERIFY_REQUESTS'] = True
    app.config['ASK_VERIFY_TIMESTAMP_DEBUG'] = True
    app.run(debug=True)

