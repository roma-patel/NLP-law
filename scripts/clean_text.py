import numpy as np
import math
import json
import urllib
import bs4
from bs4 import BeautifulSoup
import nltk
from nltk import word_tokenize
from nltk import pos_tag
import json
import re

prefix = "https://www.law.cornell.edu"
dict_def_terms = {}
def_gloss = {}

def flatten(list):
    final_list = []
    for inner_list in list:
        for item in inner_list:
            final_list.append(item)
    return final_list

def join_terms(list, start_index, end_index):
    sent = ''
    for i in range(start_index, end_index):
        sent += list[i] + ' '
    return sent

def is_monotonic(index_list):
    flag = True
    for i in range(len(index_list)):
        if i != index_list[i]:
            flag = False
    return flag

def extract_text_statute(list_def, page_text):
    sents = page_text.split('.')
    new_sents = []
    for item in sents:
        if len(item) < 40:
            continue
        print item
        print 'changed'
        if re.search('\([0-9]*\)', item):
            item = re.sub('\([0-9]*\)', '', item)
        if re.search('\([A-Z]\)', item):
            item = re.sub('\([A-Z]\)', '', item)
        if re.search('\([a-z]\)', item):
            item = re.sub('\([a-z]\)', '', item)
        if re.search('\(([i])+\)', item, re.I):
            item = re.sub('\(([i])+\)', '', item)
        if re.search('\(([ivx])+\)', item, re.I):
            item = re.sub('\(([ivx])+\)', '', item)
        if re.search('Definition of [A-Z]([a-z])+ ', item):
            item = re.sub('Definition of [A-Z]([a-z])+ ', '', item)
        if re.search('Definition(s)*', item):
            item = re.sub('Definition(s)*', '', item)
        if re.search('definition[:;]', item):
            item = re.sub('definition[:;]', '', item)
        if re.search('(, ,)+', item):
            item = re.sub('(, ,)+', ' ', item)
        if re.search('( or or)+', item):
            item = re.sub('( or or)+', '', item)
        #if re.search(' ( )+', item):
         #   item = re.sub(' ( )+', ' ', item)
        if re.search('      ', item):
            item = re.sub('      ', ': ', item)
        if re.search(' ( )+', item):
            item = re.sub(' ( )+', ' ', item)
        if re.compile('[0-9]*6').match(item, 0):
            continue
        else:
            new_sents.append(item.strip() + '. ')

        print str(new_sents)

def extract_text(list_def, page_text):
    sents = page_text.split('.')
    new_sents = []
    for item in sents:
        if len(item) < 40:
            continue
        print item
        print 'changed'
        if re.search('\([0-9]*\)', item):
            item = re.sub('\([0-9]*\)', '', item)
        if re.search('\([A-Z]\)', item):
            item = re.sub('\([A-Z]\)', '', item)
        if re.search('\([a-z]\)', item):
            item = re.sub('\([a-z]\)', '', item)
        if re.search('\(([i])+\)', item, re.I):
            item = re.sub('\(([i])+\)', '', item)
        if re.search('\(([ivx])+\)', item, re.I):
            item = re.sub('\(([ivx])+\)', '', item)
        if re.search('Definition of [A-Z]([a-z])+ ', item):
            item = re.sub('Definition of [A-Z]([a-z])+ ', '', item)
        if re.search('Definition(s)*', item):
            item = re.sub('Definition(s)*', '', item)
        if re.search('definition[:;]', item):
            item = re.sub('definition[:;]', '', item)
        if re.search('(, ,)+', item):
            item = re.sub('(, ,)+', ' ', item)
        if re.search('( or or)+', item):
            item = re.sub('( or or)+', '', item)
        if re.search(' ( )+', item):
            item = re.sub(' ( )+', ' ', item)
        if re.compile('[0-9]*6').match(item, 0):
            continue
        else:
            new_sents.append(item.strip() + '. ')

    index_list, index = [], 0
    for item in new_sents:
        if '"' in item:
            index_list.append(index)
        index += 1

    new_list, new_item = [], ''

    #print str(index_list)
    index, prev_index = 0, 0
    if len(index_list) == 0:
        return

    if index_list[0] != 0:
        end_index = index_list[0]-1
        new_item = join_terms(new_sents, 0, end_index)
        new_list.append(new_item)
        prev_index = end_index + 1
        index += 1
    for i in range(index, len(index_list)):
        if len(index_list) == 1:
            new_list = new_sents
            break
        end_index = index_list[i]-1
        new_item = ''
        for j in range(prev_index, end_index+1):
            new_item += new_sents[j]
        prev_index = end_index+1
        new_list.append(new_item)
    new_item = ''
    for i in range(index_list[len(index_list)-1], len(new_sents)):
        new_item += new_sents[i]
    new_list.append(new_item)

    for item in new_list:
        quote = re.findall('"[A-Z -]*"', item, re.I)
        squote = str(quote)
        if squote in def_gloss.keys():
            old_length = len(def_gloss[squote])
            new_length = len(item)
            if old_length < new_length:
                def_gloss[squote] = item
        else:
            def_gloss[squote] = item
        if len(quote) == 0:
            continue
        print item
        #ff.write(str(quote) + ': ' + str(item))
        #ff.write('\n\n')

def get_num(page_text, num, list):
    page_text = page_text.replace(u'\u201c', '"')
    page_text = page_text.replace(u'\u201d', '"')
    page_text = page_text.encode('ascii', 'ignore')
    list1 = re.findall('"[a-z,0-9 ]*"', page_text, re.I)
    #print str(page_text)
    #print list1
    extract_text_statute(list1, page_text)
    num += len(list1)
    list.extend(list1)
    return num, list

def get_definition_page(map, num, list):
    #takes in a chapter
    '''for key in map:
        if re.search('definition(s)*', key, re.I):
            if type(map[key]) is dict:
                num, list = get_definition_page(map[key], num, list)
            else:
                num, list = get_num(map[key], num, list)
        else:
            if type(map[key]) is dict:
                num, list = get_definition_page(map[key], num, list)'''
    for key in map:
        if type(map[key]) is dict:
            num, list = get_definition_page(map[key], num, list)
        else:
            num, list = get_num(map[key], num, list)

    return num, list

def get_any_page(map, num, list):
    return

def per_title():
    count = 1
    #newf = open('def.txt', 'w+')
    final_dict = {}
    with open('data.json', 'r') as f:
        for line in f:
            a = json.loads(line)

        for title in sorted(a):
            if count ==2: break
            count += 1#
            print 'Title'
            num, list = get_definition_page(a[title], 0, [])
            vocab_dict = {}
            final_dict[title] = {}
            for word in list:
                if word not in vocab_dict.keys():
                    vocab_dict[word] = 1
                else:
                    vocab_dict[word] += 1
            final_dict[title] = vocab_dict

           # print vocab_dict
    return final_dict

if __name__ == '__main__':
    dict = per_title()
    count = 0
    for keys in def_gloss:
        if count == 10:
            break
        count += 1
        print keys
        print def_gloss[keys]