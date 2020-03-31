import threading
from smtplib import SMTPException

import sentry_sdk
from flask import copy_current_request_context
from flask_mail import Message

from src.extensions import MAIL


def send_email(message_list=None, message=None):
    """
    This opens a connection and sends all the mails.

    If a single message is given, it will override the message list.
    :param message: One Flask Message to be sent
    :param message_list: list of Flask Messages to be sent
    :return: None
    """
    if message:
        message_list = [message]

    @copy_current_request_context
    def send_messages(messages):
        """
        This is the function, the thread should run to send mails, without the user should wait for
        this to finish, before rendering the response html.
        :param messages: List of messages to be sent.
        :return: None
        """
        with MAIL.connect() as conn:
            for message_element in messages:
                try:
                    conn.send(message_element)
                except SMTPException as e:
                    sentry_sdk.capture_message("Mail exception: '%s'." % str(e))
                except TypeError as e:
                    sentry_sdk.capture_message("TypeError exception: '%s" % str(e))
                except TimeoutError as e:
                    sentry_sdk.capture_message(
                        "A TimeOut have occurred while trying to send a mail\n%s" % str(e))

    try:
        sender_thread = threading.Thread(name="mail_sender", target=send_messages,
                                         args=(message_list,))
        sender_thread.start()
    except TypeError as e:
        sentry_sdk.capture_message("This is event occurred when trying to send mails in threads")
        sentry_sdk.capture_exception(e)


def send_confirmation_email(user):
    msg = Message(subject="Email confirmation", recipients=[user.email])
    msg.html = f"http://creditoro.nymann.dev/confirm?token={user.generate_confirmation_token()}"
    send_email(message=msg)
