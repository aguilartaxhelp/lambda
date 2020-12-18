import json
import sendgrid
import os
from sendgrid.helpers.mail import *


def sendmail(event, context):
    data = json.loads(event["body"])

    name = data["name"]
    email = data["email"]
    message = data["message"]
    subject = data["subject"]

    if not subject:
        subject = name + "'s tax inquiry"

    msg = "Name: {name}\n\nEmail: {email}\n\nMessage: {message}".format(
        name = name,
        email = email,
        message= message)

    # TODO trigger rate limits on apigw

    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(os.environ.get('FROM_EMAIL'))
    to_email = To(os.environ.get('TO_EMAIL'))
    content = Content("text/plain", msg)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


    return {
        'statusCode': 204
    }

