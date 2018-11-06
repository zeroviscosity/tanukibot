import random
import re
import time
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from .core import Core


class SMSBot(Core):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.app = Flask(__name__)
        self.app.add_url_rule('/sms', 'sms', self.incoming_sms, methods=['GET', 'POST'])

    def connect(self):
        print('TanukiBot connected and running!')
        self.app.run(debug=True, host='0.0.0.0')

    def incoming_sms(self):
        body = request.values.get('Body', None)
        if not body:
            return self.fallback()

        reply = self.get_sentence(body)
        if not reply:
            reply = self.fallback()

        resp = MessagingResponse()
        resp.message(reply)

        return str(resp)
