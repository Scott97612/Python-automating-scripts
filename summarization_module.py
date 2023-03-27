# text summarization class module

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.matcher import Matcher
from string import punctuation


class Summarization():

    @staticmethod
    def create_doc(text, model):
        try:
            if model == 'sm':
                nlp = spacy.load('en_core_web_sm')
            elif model == 'md':
                nlp = spacy.load('en_core_web_md')
            elif model == 'lg':
                nlp = spacy.load('en_core_web_lg')

            doc = nlp(text)
            return nlp, doc
        except Exception as error:
            print('Please check file directory and filename, and the model name.')

    @staticmethod
    def get_sentences(doc):
        sentences = list(doc.sents)
        return sentences

    @staticmethod
    def get_token_frequency(doc):
        # calculate the word frequencies of each word token in the doc
        stopwords = list(STOP_WORDS)
        global punctuation
        punctuation = punctuation + '\n'
        tokens = [token.text for token in doc]
        token_freq = {}
        for token in tokens:
            if token.lower() not in stopwords:
                if token.lower() not in punctuation:
                    if token not in token_freq.keys():
                        token_freq[token] = 1
                    else:
                        token_freq[token] += 1
        max_token_freq = max(token_freq.values())
        for token in token_freq.keys():
            token_freq[token] = token_freq[token] / max_token_freq
        return token_freq

    @staticmethod
    def sent_score_via_token_freq(sentences, token_freq,
                                  select_rate):  # sentences -- a list, token_freq -- a dict, select_rate -- a float
        # calculate sentence importance based on token frequencies
        sent_scores, sent_sum = {}, []
        for sent in sentences:
            for token in sent:
                if token.text.lower() in token_freq.keys():
                    if sent not in sent_scores.keys():
                        sent_scores[sent] = token_freq[token.text.lower()]
                    else:
                        sent_scores[sent] += token_freq[token.text.lower()]
        for sent in sent_scores.keys():
            sent = sent.text

        select_len = int(len(sent_scores.keys()) * select_rate+1)
        if select_len < 1:
            raise Exception('Minimum required amount not met.')
        else:
            sent_scores = {k: v for k, v in sorted(sent_scores.items(), key=lambda item: item[1])}
            sent_scores_keys = list(sent_scores.keys())
            for i in range(0, select_len - 1):
                sent_sum.append(sent_scores_keys.pop())
        try:
            summary = ''
            for sent in sent_sum:
                summary += f'\n{sent}\n=============================================='
            return sent_sum, summary
        except Exception as error:
            print('Error:' + str(error))

    @staticmethod
    def proper_noun_frequency(nlp, doc):
        # get proper Nouns frequency
        matcher = Matcher(nlp.vocab)
        patterns = [{"POS": "PROPN", "OP": "+"}]
        matcher.add("PROPER_NOUNS", [patterns], greedy='LONGEST')
        matches = matcher(doc)
        proper_nouns = []
        for match in matches:
            proper_nouns.append(doc[match[1]:match[2]])
        pn_stat, matches_text = {}, []
        for i in range(len(proper_nouns)):
            matches_text.append(proper_nouns.pop().text)
            if matches_text[i] not in pn_stat.keys():
                pn_stat[matches_text[i]] = 1
            else:
                pn_stat[matches_text[i]] += 1
        pn_stat = {k: v for k, v in sorted(pn_stat.items(), key=lambda item: item[1])}
        return pn_stat

    @staticmethod
    def sent_score_via_proper_noun(pn_stat, sentences,
                                   select_rate):  # pn_stat -- a dict, sentences -- a list, select_rate -- a float
        # grade importance on sentences via proper nouns
        rated_pn_matches = []
        stat_keys = list(pn_stat.keys())
        select_len = int(len(stat_keys) * select_rate+1)
        if select_len < 1:
            raise Exception('Minimum required amount not met.')


        try:
            for i in range(select_len):
                rated_pn_matches.append(stat_keys.pop())
            rated_sentences = []
            for key in rated_pn_matches:
                for sent in sentences:
                    if key in sent.text:
                        if sent not in rated_sentences:
                            rated_sentences.append(sent)
                        else:
                            continue
            summary = ''
            for sent in rated_sentences:
                summary += f'\n{sent}\n=============================================='
            return rated_sentences, summary

        except Exception as error:
            print('Error:' + str(error))

    @staticmethod
    def sent_sum_via_composition(doc):
        # sum up each sentence via its composition analysis
        shortened_sents = []
        pos_sift = ['AUX', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'SCONJ', 'SYM',
                    'VERB']  # Part of Speech tags to sift through the doc text
        for sent in doc.sents:
            sent_list = []
            for token in sent:
                if token.pos_ in pos_sift:
                    sent_list.append(token)
            shortened_sents.append(sent_list)

        summary = ''
        for sent in shortened_sents:
            sentence = ''
            for token in sent:
                sentence += f'{token.text} '
            sentence = sentence.rstrip(' ') + '.'
            summary += f'\n{sentence}\n'
        return shortened_sents, summary