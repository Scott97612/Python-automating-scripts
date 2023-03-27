#! python3.10

# stores the passwords for assorted accounts
import sys, pyperclip

PASSWORDS = {
    'email':'12345',
    'game':'78945',
    'github':'45612',
    'youtube':'15978',
}

if len(sys.argv) < 2:
    print('Usage: py password.py [account] - copy account password')
    sys.exit()

account = sys.argv[1]

if account in PASSWORDS:
    pyperclip.copy(PASSWORDS[account])
    print('Password for' + account + ' copied to clipboard.')
else:
    print('There is no account named' + account)