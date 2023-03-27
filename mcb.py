#! python3.10
# multiclipboard

import sys, pyperclip, shelve

mcb_shelf = shelve.open('mcb')


if len(sys.argv) == 3 and sys.argv[1].lower() == 'save':
    # e.g., command line: "mcb(argv[0]) save(argv[1]) one(argv[2])" ----the length of argv is 3

    mcb_shelf[sys.argv[2]] = pyperclip.paste()
    # 'one' becomes the keyword for the content I just copied.
elif len(sys.argv) == 2:
    if sys.argv[1].lower() == 'list':
        # e.g., command line: "mcb(argv[0]) list(argv[1]) ----the length of argv is 2

        print(str(list(mcb_shelf.keys())))  # all keywords stored so far printed to terminal.

    elif sys.argv[1] in mcb_shelf:
        # e.g., command line: "mcb(argv[0]) one(argv[1])" ----the length of argv is 2

        pyperclip.copy(mcb_shelf[sys.argv[1]])
        # keyword 'one' corresponds a stored content which is copied to the clipboard.

mcb_shelf.close()