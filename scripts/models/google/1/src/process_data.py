import numpy as np
import cPickle
from collections import defaultdict
import sys, re
import pandas as pd
folder_path = '/nlp/data/romap/law/task_2/'
path = folder_path + 'scripts/cnn/'

def build_data_cv(data_folder, cv=10, clean_string=True):
    """
    Loads data and split into 10 folds.
    """
    '''revs = []
    pos_file = data_folder[0]
    neg_file = data_folder[1]
    vocab = defaultdict(float)
    count_pos, count_neg = 0, 0
    with open(pos_file, "rb") as f:
        for line in f:
            count_pos += 1
            rev = []
            rev.append(line.strip())
            if clean_string:
                orig_rev = clean_str(" ".join(rev))
            else:
                orig_rev = " ".join(rev).lower()
            words = set(orig_rev.split())
            for word in words:
                vocab[word] += 1
            datum  = {"y":1, 
                      "text": orig_rev,                             
                      "num_words": len(orig_rev.split()),
                      "split": np.random.randint(0,cv)}
            revs.append(datum)
    with open(neg_file, "rb") as f:
        for line in f:
            count_neg += 1
            rev = []
            rev.append(line.strip())
            if clean_string:
                orig_rev = clean_str(" ".join(rev))
            else:
                orig_rev = " ".join(rev).lower()
            words = set(orig_rev.split())
            for word in words:
                vocab[word] += 1
            datum  = {"y":0, 
                      "text": orig_rev,                             
                      "num_words": len(orig_rev.split()),
                      "split": np.random.randint(0,cv)}
            revs.append(datum)
    return revs, vocab'''

    revs, chars = [], []
    train_file = data_folder[0]; test_file = data_folder[1]
    vocab = defaultdict(float); count_1, count_2, count_3 = 0, 0, 0

    f = open(train_file, 'r')
    for line in f:
        items = line.strip().split('\t')
        word = items[0]; num_words = len(word)*2; fin_word = word + ' '
        for char in word:
            vocab[char] += 1
            fin_word += char + ' '
        datum = {"y": int(items[1]), "text": fin_word.strip(), "num_words": num_words, "split": np.random.randint(0,cv)} 
        revs.append(datum)
        vocab[items[0]] += 1

    f = open(test_file, 'r')
    for line in f:
        items = line.strip().split('\t')
        word = items[0]; num_words = len(word)*2; fin_word = word + ' '
        for char in word:
            vocab[char] += 1
            fin_word += char + ' '
        datum = {"y": int(items[1]), "text": fin_word, "num_words": num_words, "split": np.random.randint(0,cv)} 
        revs.append(datum)
        vocab[items[0]] += 1

    return revs, vocab
    
def get_W(word_vecs, k=300):
    """
    Get word matrix. W[i] is the vector for word indexed by i
    """
    vocab_size = len(word_vecs)
    word_idx_map = dict()
    W = np.zeros(shape=(vocab_size+1, k), dtype='float32')            
    W[0] = np.zeros(k, dtype='float32')
    i = 1
    for word in word_vecs:
        W[i] = word_vecs[word]
        word_idx_map[word] = i
        i += 1
    return W, word_idx_map

def load_bin_vec(fname, vocab):
    """
    Loads 300x1 word vecs from Google (Mikolov) word2vec
    """
    word_vecs = {}
    with open(fname, "rb") as f:
        header = f.readline()
        vocab_size, layer1_size = map(int, header.split())
        binary_len = np.dtype('float32').itemsize * layer1_size
        for line in xrange(vocab_size):
            word = []
            while True:
                ch = f.read(1)
                if ch == ' ':
                    word = ''.join(word)
                    break
                if ch != '\n':
                    word.append(ch)   
            if word in vocab:
               word_vecs[word] = np.fromstring(f.read(binary_len), dtype='float32')  
            else:
                f.read(binary_len)

    #load character vecs
    f = open(folder_path + '/data/glove.840B.300d-char.txt', 'r')
    lines = f.readlines()[1:]
    for line in lines:
        items = line.strip().split(' ')
        word, vec = items[0], [float(i) for i in items[1:]]
        if word in vocab:
            word_vecs[word] = vec
                
    return word_vecs

def add_unknown_words(word_vecs, vocab, min_df=1, k=300):
    """
    For words that occur in at least min_df documents, create a separate word vector.    
    0.25 is chosen so the unknown vectors have (approximately) same variance as pre-trained ones
    """
    for word in vocab:
        if word not in word_vecs and vocab[word] >= min_df:
            word_vecs[word] = np.random.uniform(-0.25,0.25,k)  

def clean_str(string, TREC=False):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Every dataset is lower cased except for TREC
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
    return string.strip() if TREC else string.strip().lower()

def clean_str_sst(string):
    """
    Tokenization/string cleaning for the SST dataset
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)   
    string = re.sub(r"\s{2,}", " ", string)    
    return string.strip().lower()

if __name__=="__main__":
    global w2v_name, set_name
    w2v_file, w2v_name, set_name = sys.argv[1], sys.argv[2], sys.argv[3]
    dataset_path = path + w2v_name + '/' + set_name + '/'
    #data_folder = [path + "/data/cases.pos", path + "/data/cases.neg"]    
    data_folder = ['/nlp/data/romap/law/task_2/data/train_words.txt', '/nlp/data/romap/law/task_2/data/test_words.txt']
    print "loading data...",        
    revs, vocab = build_data_cv(data_folder, cv=10, clean_string=True)
    f = open(path + '/' + w2v_name + '/data/vocab.txt', 'w+')
    for word in sorted(vocab):
        f.write(word + '\n')
    max_l = np.max(pd.DataFrame(revs)["num_words"])
    print "data loaded!"
    
    print "number of sentences: " + str(len(revs))
    print "vocab size: " + str(len(vocab))
    print "max sentence length: " + str(max_l)
    print "loading word2vec vectors...",
    w2v = load_bin_vec(w2v_file, vocab)
    print "word2vec loaded!"
    print "num words already in word2vec: " + str(len(w2v))
    add_unknown_words(w2v, vocab)
    W, word_idx_map = get_W(w2v)
    rand_vecs = {}
    add_unknown_words(rand_vecs, vocab)
    W2, _ = get_W(rand_vecs)
    cPickle.dump([revs, W, W2, word_idx_map, vocab], open(dataset_path + "/data/mr.p", "wb"))
    print "dataset created!"


    
    
