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
    return compliment_teller()

    
@ask.intent("AMAZON.StopIntent")
def stop_function():
    return statement("See you tomorrow")

    
@ask.intent("AMAZON.CancelIntent")
def cancel_function():
    return statement("See you tomorrow")


@ask.launch
def launched():
    return compliment_teller()

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
        return compliment_teller()


#--------------- App Functions ------------------------
def compliment_teller():
    session_attributes = {}
    card_title = "Daily inspiration"
    compliment = get_compliment()
    speech_output = "The truth is... "+compliment
    reprompt_text = compliment
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_compliment():
    now = datetime.datetime.now()
    day = now.day
    return compliments_list[int(day)%10]


#---------------- Food List ----------------------------
#BURAYA_YENI_STRINGLER
compliments_list = ("Wow, you shine bright like a diamond today.", "I can't think of anyone that could resist your charm.", "You should be proud of yourself, you are awesome.", "You're even more beautiful on the inside than you are on the outside.", "You don't need any inspiration, I am inspired by you!", "You are so good that you bring out the best in other people.", "I love your style, you are my icon.", "You're like sunshine on a rainy day.", "Colors seem brighter when you're around.", "People are lucky to have you around.", "You're like a candle in the darkness. ", "Being around you is like a happy little vacation." )


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.config['ASK_APPLICATION_ID'] = 'amzn1.ask.skill.032dbe18-8f0f-4620-b594-94a20853c97c'
    app.config['ASK_VERIFY_REQUESTS'] = True
    app.config['ASK_VERIFY_TIMESTAMP_DEBUG'] = True
    app.run(debug=True)

