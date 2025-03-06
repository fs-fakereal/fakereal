# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from forms import Email

message = Mail(
    from_email='fakeRe.41@gmail.com',
    to_emails= Email,
    subject='Verify your Email - FakeReal',
    html_content='<strong>Verify your email address\nYou need to verify your email address to continue using your FakeReal account.</strong>')
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)