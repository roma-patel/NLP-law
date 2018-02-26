import numpy as np
import re
import itertools
from collections import Counter
path = '/nlp/data/romap/law/task_2/scripts/cnn/google/1/'
path = '/Users/romapatel/Desktop/law/task_2/scripts/cnn/google/1/'

def load_data_and_labels(positive_data_file, negative_data_file):
    """
    Loads words for 3 classes, splits the data into words + chars and labels.
    Returns sentences = word + chars and labels.
    """
    # Load data from files

    words, labels = [], []
    f = open('/nlp/data/romap/law/task_2/data/train_words.txt', 'r')
    for line in f:
        items = line.strip().split('\t')
        word, label = items[0], items[1]; fin_word = word + ' '
        for char in word: fin_word += char + ' '
        words.append(fin_word.strip()); labels.append(label)

    lookup = {'0': [1, 0, 0], '1': [0, 1, 0], '2': [0, 0, 1]}
    fin_labels = [lookup[i] for i in labels]

    #for i in range(len(words)):
        #print words[i]; print fin_labels[i]; print '\n'
    y = np.concatenate([fin_labels], 0)
    return [words, y]


def batch_iter(data, batch_size, num_epochs, shuffle=True):
    """
    Generates a batch iterator for a dataset.
    """
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int((len(data)-1)/batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]

def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()
