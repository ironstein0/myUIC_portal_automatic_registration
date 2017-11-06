from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "ACf0aef2aa51691015a960daff390dce3d"
# Your Auth Token from twilio.com/console
auth_token  = "3a106836d08c12faa2215b2ab99c60d2"

def send_sms(message_body):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=     "+18723339826", 
        from_=  "+16307915714",
        body=   message_body
    )

    print(message.sid)
