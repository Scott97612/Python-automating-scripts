#! python3.10
# used to extract phone numbers (Chinese ones) and email addresses

import re, pyperclip

phone_regex = re.compile(r'''(
    ([+][8][6])?            # country code optional
    ([1]\d{2})              # start with number "1", first 3 digits
    ([-]|[\s])?             # optional sign to specify phone number format
    (\d{4})                 # middle 4 digits
    ([-]|[\s])?             # optional sign to specify phone number format
    (\d{4})                 # last 4 digits
)''', re.VERBOSE)

email_regex = re.compile(r'''(
    [a-zA-Z0-9._%+-]+       # user name
    [@]                     # at sign
    [a-zA-Z0-9.-]+          # domain name
    (\.[a-zA-Z]{2,4})       # dot something
)''', re.VERBOSE)


text = str(pyperclip.paste())
p_matches, e_matches = [], []

for groups in phone_regex.findall(text):
    phone_number = '+86 '+'-'.join([groups[2], groups[4], groups[6]])
    p_matches.append(phone_number)
for groups in email_regex.findall(text):
    e_matches.append(groups[0])

p_matches.sort()
e_matches.sort()
all_matches = p_matches + e_matches

if len(all_matches) > 0:
    pyperclip.copy('\n'.join(all_matches))
    print('Sorted and copied to clipboard:\n')
    for i in all_matches:
        print(f'{i}\n')
else:
    print('No phone numbers or email addresses detected.')