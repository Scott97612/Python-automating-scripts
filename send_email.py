#! python3.10
# email automate
# uses send_auto_email_module.py

import sys
import send_auto_email_module

def confirm_command(text):
    if len(sys.argv) == 1:
        send_auto_email_module.get_server_and_send_auto(text)
    else:
        receiver = ''.join(sys.argv[1:])
        send_auto_email_module.get_server_and_send_auto(text,receiver=receiver)

if __name__ == '__main__':
    type_in = input('Input the body of the email:\n')
    confirm_command(type_in)
    print('If no error message displayed, then email successfully sent.')



