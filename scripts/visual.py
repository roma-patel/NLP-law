import sys
import codecs
import numpy as np
import matplotlib.pyplot as plt
import math

from sklearn.manifold import TSNE
file_name = 'wvec.txt'

def main():
    embeddings_file = 'wvec.txt'
    wv, vocabulary = load_embeddings(embeddings_file)
    wv = wv[1:]
    for i in range(len(wv)):
        if math.isnan(wv[i]) or math.isinf(wv[i]):
            wv[i] = 0.0045
    wv = wv.reshape(-1,1)
    tsne = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    print'yes'
    Y = tsne.fit_transform(wv[:50])
    print 'no'
    plt.scatter(Y[:, 0], Y[:, 1])
    for label, x, y in zip(vocabulary, Y[:, 0], Y[:, 1]):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
    plt.show()


def load_embeddings(file_name):
    with codecs.open(file_name, 'r', 'utf-8') as f_in:
        vocabulary, wv = zip(*[line.strip().split(' ', 1) for line in
                               f_in])
    wv = np.loadtxt(wv)
    return wv, vocabulary


if __name__ == '__main__':
    main()
