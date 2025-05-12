from flask import render_template, current_app, url_for
from flask_mail import Message
from app import mail
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()

def send_confirmation_email(user):
    token = user.get_email_verification_token()
    send_email('EcoTrack: Please confirm your email',
               sender=current_app.config['MAIL_DEFAULT_SENDER'],
               recipients=[user.email],
               text_body=render_template('email/confirm_email.txt',
                                         user=user, token=token),
               html_body=render_template('email/confirm_email.html',
                                         user=user, token=token))

def send_email_update_confirmation(user, new_email):
    """
    Sends a confirmation email to the new address during an email update.
    """
    token = user.get_email_update_token(new_email)
    confirm_url = url_for('main.confirm_email', token=token, _external=True)

    send_email(
        'EcoTrack: Confirm your new email address',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[new_email],
        text_body=render_template('email/confirm_email.txt', user=user, token=token),
        html_body=render_template('email/confirm_email.html', user=user, token=token)
    )
    
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('EcoTrack: Password Reset Request',
               sender=current_app.config['MAIL_DEFAULT_SENDER'],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))