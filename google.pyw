#! python3.10
# get google (or map) search results

import webbrowser, sys, pyperclip

def get_page(url):
    webbrowser.open(url)

def confirm_command():
    if len(sys.argv) == 1:
        url = f'https://www.google.com/search?q={pyperclip.paste()}&newwindow'
        get_page(url)
    else:
        if sys.argv[1] == 'map':
            if len(sys.argv) == 2:
                url = f'https://www.google.com/maps/place/{pyperclip.paste()}'
                get_page(url)
            else:
                attach = '+'.join(sys.argv[2:])
                url = f'https://www.google.com/maps/place/{attach}'
                get_page(url)

        else:
            attach = '+'.join(sys.argv[1:])
            url = f'https://www.google.com/search?q={attach}&newwindow'
            get_page(url)

if __name__ == "__main__":
    confirm_command()