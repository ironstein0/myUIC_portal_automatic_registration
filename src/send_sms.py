from twilio.rest import Client
from config import credentials

account_sid = credentials.ACCOUNT_SID
auth_token = credentials.AUTH_TOKEN
twilio_number = credentials.TWILIO_NUMBER
phone_numbers = credentials.USER_PHONE_NUMBER

def send_sms(message_body):
    client = Client(account_sid, auth_token)

    for phone_number in phone_numbers:
        message = client.messages.create(
            to=     phone_number, 
            from_=  twilio_number,
            body=   message_body
        )

        print(message.sid)