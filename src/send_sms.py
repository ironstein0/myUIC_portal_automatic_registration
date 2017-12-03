from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "ACf517d947feec9a53125b26ae9c9aad17"
# Your Auth Token from twilio.com/console
auth_token  = "654b649c1999a5e9b4dbe2c94687a7d6"
# Twilio Phone Number
twilio_number = '+14243040690'
# My phone numbe

def send_sms(message_body):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=     "+18723339826", 
        from_=  twilio_number,
        body=   message_body
    )

    print(message.sid)

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=     "+13127926471", 
        from_=  twilio_number,
        body=   message_body
    )

    print(message.sid)

    # message = client.messages.create(
    #     to=     "+13128387836", 
    #     from_=  "+16307915714",
    #     body=   message_body
    # )

    # print(message.sid)