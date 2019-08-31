import pandas as pd
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize


def load_data():
    """
    load dataset for stemming
    return dataset
    """
    data = pd.read_csv('kamus.txt', sep='\t')
    return data


def look_for_imbuh(context):
    """
    parameter is list input
    return the result of a word which processes from stemming
    """
    data = load_data()
    imbuhan = data.iloc[:, 1].values
    i = 0
    for item in imbuhan:
        if item == context:
            return data.iloc[i, 0]
        i += 1
    return False


def load_model():
    """
    to load model word2vec
    return model word2vec
    """
    model = Word2Vec.load("id.bin")
    model.init_sims(replace=True)
    return model


def check_in_word2vec(w1, w2v):
    """
    to tokenize input sentence
    returning list of all words from sentence
    """
    token = word_tokenize(w1)
    for item in token:
        temp = item
        stem = look_for_imbuh(item)

        if stem:
            temp = stem

        if temp not in w2v:
            token.remove(item)
    return token


def count_max(word1, word2, model, w2v):
    """
    to count between two words in difference sentence which have a big weight similarity
    return weigt similarity between two sentence and how many word being processed
    """
    w1 = check_in_word2vec(word1, w2v)
    w2 = check_in_word2vec(word2, w2v)

    ww1 = word_tokenize(word1)
    ww2 = word_tokenize(word2)

    temp, y, count = 0, 0, 0
    temp1, y1 = 0, 0
    unik, listtt = [], []

    for item in ww1:
        if (item not in unik) and (item not in w1) and (item not in w2) and (item in ww2):
            unik.append(item)
            count = 1
            listtt.append(1)
            y1 += 1
    if count != 0:
        temp1 += 0 if len(listtt) == 0 else max(listtt)

    temp, y, count = 0, 0, 0
    for i in w1:
        listt = []
        count = 0

        if i in w2v:
            count = 1
            y += 1

        for j in w2:
            if i in w2v and j in w2v:
                listt.append(model.similarity(i, j))
        if count != 0:
            temp += 0 if len(listt) == 0 else max(listt)
    return temp, temp1, y, y1


def check_treshold(w1, w2):
    """
    to assign threshold for a sentence can be similar
    return True if two sentence are similar, and False if the opposite
    """
    model = load_model()
    w2v = list(model.wv.vocab)

    temp, temp1, y, y1 = count_max(w1.lower(), w2.lower(), model, w2v)
    temp += temp1
    y += y1

    threshold = 0.45
    if temp > 0:
        return temp/y > threshold
    else:
        return False


if __name__ == "__main__":
    word1 = input('kata 1: ')
    word2 = input('kata 2: ')
    print(check_treshold(word1, word2))
