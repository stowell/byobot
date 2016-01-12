import base64
from flask import (
    Flask,
    make_response,
    request,
)
import json
import urllib

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

import bs4


class TwilioSms(ndb.Model):
    message_sid = ndb.StringProperty()
    account_sid = ndb.StringProperty()
    messaging_service_sid = ndb.StringProperty()
    sending_phone_number = ndb.StringProperty()
    receiving_phone_number = ndb.StringProperty()
    body = ndb.StringProperty()
    num_media = ndb.IntegerProperty()


app = Flask(__name__)


def post2sms(request):
    twilio_sms = TwilioSms(
        message_sid=request.form.get('MessageSid', ''),
        account_sid=request.form.get('AccountSid', ''),
        messaging_service_sid=request.form.get('MessagingServiceSid', ''),
        sending_phone_number=request.form.get('From', ''),
        receiving_phone_number=request.form.get('To', ''),
        body=request.form.get('Body', ''),
        num_media=int(request.form.get('NumMedia', 0)),
    )
    return twilio_sms


def get2sms(request):
    twilio_sms = TwilioSms(
        message_sid=request.args.get('MessageSid', ''),
        account_sid=request.args.get('AccountSid', ''),
        messaging_service_sid=request.args.get('MessagingServiceSid', ''),
        sending_phone_number=request.args.get('From', ''),
        receiving_phone_number=request.args.get('To', ''),
        body=request.args.get('Body', ''),
        num_media=int(request.args.get('NumMedia', 0)),
    )
    return twilio_sms


def sms2twiml(twilio_sms):
    xml = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>
        <Body>{0}</Body>
    </Message>
</Response>'''.format(twilio_sms.body)
    response = make_response(xml, 200)
    response.headers['Content-Type'] = 'text/xml'
    return response

@app.route('/echo', methods=('GET',))
def echo_get():
    twilio_sms = get2sms(request)
    twilio_sms.put()
    return sms2twiml(twilio_sms)

@app.route('/echo', methods=('POST',))
def echo_post():
    twilio_sms = post2sms(request)
    twilio_sms.put()
    return sms2twiml(twilio_sms)

@app.route('/notify', methods=('GET',))
def notify():
    wunderground_response = urlfetch.fetch('http://api.wunderground.com/api/ddacf80a930e9c48/conditions/q/MA/Cambridge.json')
    if wunderground_response.status_code == 200:
        temp_string = str(json.loads(wunderground_response.content)['current_observation']['temp_f'])
        auth_string = 'Basic %s' % base64.b64encode('ACabe6ec7002f2e9c94a6d44a9ee8c64a8:c378ec162520b4f3879ac76559ae6905')
        form_string = urllib.urlencode({
            'To': '+13125456355',
            'From': '+18722405072',
            'Body': 'It\'s %s out' % temp_string,
        })
        urlfetch.fetch(
            'https://api.twilio.com/2010-04-01/Accounts/ACabe6ec7002f2e9c94a6d44a9ee8c64a8/Messages.json',
            headers={
                'Authorization': auth_string,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            method=urlfetch.POST,
            payload=form_string,
        )
    return ('', 204)

@app.route('/tw', methods=('GET',))
def tw():
    soup = bs4.BeautifulSoup(urlfetch.fetch('https://twitter.com/paulg').content, 'html.parser')
    a_tweet = soup.find(name='p', attrs={'class': 'TweetTextSize'}).text
    return (a_tweet, 200)

