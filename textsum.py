#! python3.10
# run text summarization
# uses summarization_module.py and sum_interface.py

from sum_interface import Interface

if __name__ == '__main__':
    run = True
    while run:
        Interface.confirm_command()
        indicator = input('Run another turn? "y" or "n".')
        if indicator == 'n':
            run = False
        else: continue