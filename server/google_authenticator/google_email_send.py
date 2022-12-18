import base64
from google_authenticator import get_service
from email.message import EmailMessage

from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def create_message(to, subject, body):
    message = EmailMessage()
    message["To"] = to
    message["Subject"] = subject
    message["From"] = "bubblesarepretty126@gmail.com"
    message.add_alternative(body, subtype="html")
    return base64.urlsafe_b64encode(message.as_bytes()).decode()


def gmail_send(email, subject, content):
    """Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    service = get_service()

    try:
        # encoded message
        encoded_message = create_message(email, subject, content)

        created_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=created_message).execute())
        print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message
