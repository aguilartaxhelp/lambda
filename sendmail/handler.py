import json
import sendgrid
import os


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


    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
    from_email = os.environ.get("FROM_EMAIL")
    to_email = os.environ.get("TO_EMAIL")
    bot_name = os.environ.get("BOT_NAME")
    to_name = os.environ.get("TO_NAME")
    data = {
      "personalizations": [
        {
          "to": [
            {
              "email": to_email,
              "name": to_name
            }
          ],
          "subject": bot_name + ": " + subject
        }
      ],
      "from": {
        "email": from_email,
        "name": bot_name
      },
      "reply_to": {
        "email": email,
        "name": name
      },
      "content": [
        {
          "type": "text/plain",
          "value": msg
        }
      ]
    }
    response = sg.client.mail.send.post(request_body=data)
    print(response.status_code)
    print(response.body)
    print(response.headers)


    return {
        'statusCode': 204
    }
