import json
import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk import word_tokenize
import pyth
from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter

def get_text_rtf(filename):
    doc = Rtf15Reader.read(open(filename))
    text = PlaintextWriter.write(doc).getvalue()
    return text

def get_key(fileid):
    key = fileid.split(' ')[0]
    key = key.split('-')[0]
    key = key.split('_')[0]
    key = key.split('.')[0]
    return key

def get_level_dict():
    f = open('/Users/romapatel/Desktop/statutes/levels.json', 'r')
    for line in f:
        level_dict = json.loads(line)
    count = 0
    for case in level_dict:
        if case == '': continue
        flag = True
        for level in ['1', '2', '3']:
            if len(level_dict[case][level]) == 0: flag = False
        if flag is False: continue
        l_1, l_2, l_3 = level_dict[case]['1'], level_dict[case]['2'], level_dict[case]['3']
        l_1, l_2, l_3 = l_1.split(' '), l_2.split(' '), l_3.split(' ')
        print str(case) + '\t' + str(len(l_1)) + '\t' + str(len(l_2)) + '\t' + str(len(l_3))


def create_level_dict():
    level_dict = {}
    dirpath = '/Users/romapatel/Desktop/statutes/level_'
    levels = [1,2,3,4,5]
    for level in levels:
        folder_path = dirpath + str(level) + '/'
        fileids = PlaintextCorpusReader(folder_path, '.*').fileids()
        for fileid in fileids:
            print fileid
            key = get_key(fileid)
            if key not in level_dict.keys():
                level_dict[key] = {}
                for temp_level in levels:
                    level_dict[key][temp_level] = ''
            text = ''
            if '.rtf' in fileid:
                text = get_text_rtf(folder_path + fileid)
            elif '.txt' in fileid:
                with open(folder_path + fileid, 'r') as f:
                    for line in f:
                        text += line + ' '
            text = text.decode('ascii', 'ignore')
            text = text.encode('ascii', 'ignore')

            level_dict[key][level] = text

    print level_dict
    f = open('/Users/romapatel/Desktop/statutes/levels.json', 'w+')
    f.write(json.dumps(level_dict))

if __name__ == '__main__':
    get_level_dict()