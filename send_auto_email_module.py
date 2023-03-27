# send email auto module

import smtplib
from email.mime.text import MIMEText
from email.header import Header

default_receiver = '' # receiving email
default_sender = '' # sending email

def msg(text,receiver):
    message = MIMEText(text, 'plain','utf-8')
    message['From'] = default_sender
    message['To'] = receiver
    message['Subject'] = "Message from your friend Python." # email title
    return message

def get_server_and_send_auto(text, receiver=default_receiver):
    '''if only use "text" argument, use default receiver; otherwise, designate other receiver address.'''
    try:
        server_obj = smtplib.SMTP_SSL('smtp.163.com',465)
        server_obj.ehlo_or_helo_if_needed()
        server_obj.login(default_sender, '') # smtp verification code provided by email server
        message = msg(text,receiver)
        server_obj.sendmail(default_sender, receiver, message.as_string())
        server_obj.quit()
    except Exception as error:
        print('Unable to connect to server or log in or unable to send.')


