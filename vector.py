
import os
import re
import nltk
import random
import logging
import numpy as np
import string
from glob import glob
from numpy import array
from nltk import WordNetLemmatizer 
from nltk.corpus import wordnet
from gensim.models import Word2Vec
from nltk.corpus import stopwords


# Stop words
en_stop = stopwords.words('english')
en_stop.append("'d")
it_stop = stopwords.words('italian')
punctuations = list(string.punctuation)


# Functions 
def clean_sentences(sent_list):

    """""""""
    take a list of str and oprates statard corpus cleaning
    """""

    def lemmatizer(toupla):

        lm = WordNetLemmatizer()

        if toupla[1].startswith('J'):
            return lm.lemmatize((toupla[0]), wordnet.ADJ)
        elif toupla[1].startswith('V'):
            return lm.lemmatize((toupla[0]), wordnet.VERB)
        elif toupla[1].startswith('N'):
            return lm.lemmatize((toupla[0]), wordnet.NOUN)
        elif toupla[1].startswith('R'):
            return lm.lemmatize((toupla[0]), wordnet.ADV)
        else:
            return lm.lemmatize(toupla[0])

    # word tokenization
    print('tokenizing sentences')
    sn = list(np.zeros(len(sent_list)))
    for sen in range(len(sn)):
        sn[sen] = nltk.word_tokenize(sent_list[sen])

    # remove digits
    print('removing digits')
    for s in range(len(sn)):
        for tk in range(len(sn[s])):
            if sn[s][tk].isdigit():
                sn[s][tk] = '#cardinal'

    # removing stopwords and punctuation
    print('removing stop words and punctuation')
    clean_sents = list(np.zeros(len(sn)))
    for i in range(len(sn)):
        clean_sents[i] = [word.lower() for word in sn[i] if word.lower()
                          not in en_stop and word.lower() not in punctuations]

    # pos tagging
    print('pos tagging')
    tag_sent = list(np.zeros(len(clean_sents)))
    for i in range(len(clean_sents)):
        tag_sent[i] = nltk.pos_tag(clean_sents[i])

    # lemmatizing (still needs to use the pos tag)
    print('lemmatizing')
    final_sent = list(np.zeros(len(tag_sent)))
    for s in range(len(tag_sent)):
        final_sent[s] = [lemmatizer(touple) for touple in tag_sent[s]]

    return final_sent


# Preparing the corpus
print('Input directory to Word2Vec trining corpora')

corpus = input()

print('creating the corpus')
pg = []
documents = []
# Needs a folder filled with texts to read
for file in glob(corpus + os.sep + '**', recursive=True):
    if os.path.isdir(file):
        continue
    doc = open(file, 'r').read()
    documents.append(doc)
    s = nltk.sent_tokenize(doc)
    for sent in s:
        pg.append(str(sent).strip('[', ).strip(']'))

print('the corpus is done', '\nit contains', len(documents),
      'documents and', len(pg), 'sentences')

pirnt('Cleaning the collected Corpus')
final_corpus = clean_sentences(pg)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

# sentences vectorization
# set the 'new' method
languageModel = Word2Vec(fianl_corpus, size=400, min_count=0)



