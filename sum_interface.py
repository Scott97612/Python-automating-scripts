# text summarization interface
# use self-written summarization_module.Summarization

import sys, docx, pyperclip
from summarization_module import Summarization

class Interface():

    @staticmethod
    def get_text(filetype, filename):
        global text
        if filetype == 'd':
            doc = docx.Document(filename)
            full_text = []
            for paragraph in doc.paragraphs:
                full_text.append(paragraph.text)
                text = ''.join(full_text)
        elif filetype == 't':
            with open(filename, 'r', encoding='utf-8') as f:
                text = f.read()
            text = text.replace('\n', '')
        elif filetype == 'c':
            text = pyperclip.paste()
            text = text.replace('\n', '')
        else:
            print('Wrong file type or file directory.')
        return text

    @staticmethod
    def confirm_command():
        if len(sys.argv) != 1:
            print('Wrong input command keyword.')
        elif len(sys.argv) == 1:
            filetype = input('Specify the type of file, i.e. "t" for "txt", "d" for "docx" or "c" for "clipboard".')
            filename = input("Please copy and paste the absolute path of the text file. (If it's from clipboard,"
                             "pass this input.)")
            model = input('"sm":small; "md":medium; "lg":large.')
            text = Interface.get_text(filetype,filename)
            choice = input('Choose summarization method: \n"a": token frequency sum;\n"b": proper noun sum;\n'
                           '"c": composition analysis sum;\n"d": compo sum fed to token frequency sum.')
            if choice == 'a':
                select_rate = float(input('Summarization proportion: --(from 0.0 to 1.0)'))
                nlp, doc = Summarization.create_doc(text, model)
                token_freq_dict = Summarization.get_token_frequency(doc)
                sentences = Summarization.get_sentences(doc)
                sum_list, summary = Summarization.sent_score_via_token_freq(sentences, token_freq_dict, select_rate)
                print(summary)
            elif choice == 'b':
                select_rate = float(input('Summarization proportion: --(from 0.0 to 1.0)'))
                nlp, doc = Summarization.create_doc(text, model)
                pron_dict = Summarization.proper_noun_frequency(nlp,doc)
                sentences = Summarization.get_sentences(doc)
                sum_list, summary = Summarization.sent_score_via_proper_noun(pron_dict, sentences, select_rate)
                print(summary)
            elif choice == 'c':
                nlp, doc = Summarization.create_doc(text, model)
                sum_list, summary = Summarization.sent_sum_via_composition(doc)
                print(summary)
            elif choice == 'd':
                select_rate = float(input('Summarization proportion: --(from 0.0 to 1.0)'))
                nlp, doc = Summarization.create_doc(text, model)
                sum_list, summary = Summarization.sent_sum_via_composition(doc)
                doc_re = Summarization.create_doc(summary, model)
                token_freq_dict = Summarization.get_token_frequency(doc)
                sentences = Summarization.get_sentences(doc)
                sum_list, summary_re = Summarization.sent_score_via_token_freq(sentences, token_freq_dict, select_rate)
                print(summary_re)
