
# Juliana McCausland
# Ling 473
# Project 5

import codecs
import string
import os
import math
import sys
from collections import OrderedDict

def extra(diff, lang_best):
#difference threshold set at 15 -- if values have a difference less than 15 than result is unkown
    if 15 > diff:
        print("result unk")
    else:    
        print("result {}".format(lang_best))

def getfiles(cpath):
    return os.listdir(cpath)

def log_probabilities(langdict, txt, langlist, identifier, sentence):

    #add-1 smoothing
    for w in langdict:
        for lang in langdict[w]:
            langdict[w]['w_sum'] += 1
            langdict[w][lang] += 1 
    prob_dict = {}
    for lang in langlist:
        prob = float(0)
        for word in txt:
            if word in langdict:
                
                prob +=  math.log10(float(langdict[word][lang])/float(langdict[word]['w_sum']))
               
            else:
                #words not in dictionary given "singleton" probability 
                prob += math.log10(1/15)
               
        #prob += math.log10(prob)
        prob_dict[lang] = prob
    probabilities = prob_dict

    maximum = -1 * float('inf')
    lang_best = 'unk'
    
    print('{}\t{}'.format(identifier, sentence[:-1]))
    avg = 0
    for i in probabilities:
       #printing -probabilities for each language
        avg += probabilities[i]
        if probabilities[i] > maximum:
            #highest prob = best match 
            maximum = probabilities[i]
            lang_best = i 
        print('{}\t{}'.format(i,probabilities[i]))

    #finding difference for threshold for extra credit 
    diff = maximum - avg/15
    if sys.argv[3] == "False": #if not extra credit 
        print("result {}".format(lang_best))
    else: 
        extra(diff, lang_best)
   

def main():

    #cpath = '/opt/dropbox/19-20/473/project5/language-models'
  
    cpath = sys.argv[1]
    testpath = sys.argv[2]
    lang_occurrence_dict = {}
    langdict = {}
    langlist = []
   
    #open the language model files using latin_1 encoding
    files = getfiles(cpath)
    for file_name in files:
        fpath = os.path.join(cpath, file_name)
        with codecs.open(fpath,encoding='latin_1', mode='r', errors='strict') as f:
            #extract 3-letter name of language from filename 
            lang_name = file_name[:3]
            
            #create list for the 15 language names
            if lang_name not in langlist:
                langlist.append(lang_name)
                langlist.sort()

            #extracting each word and its count from language model file
            #add each word to dictionary -- so each word will have dict for its own counts in each language
            for line in f:
                line = line.split('\t')
                word = line[0]
                count = int(line[1]) 
                if word not in lang_occurrence_dict:
                    lang_occurrence_dict[word] = {'dan':0,'deu':0,'dut':0,'eng':0,'fin':0,'fra':0,'gla':0,'ita':0,'nob':0,'pol':0,'por':0,'spa':0,'swe':0,'swh':0,'tgl':0}
                lang_occurrence_dict[word][lang_name] = count
                
    #sum up the occurrences for each word
    for w in lang_occurrence_dict:
        w_sum = 0
        for language in langlist:
            w_sum += lang_occurrence_dict[w][language]
        lang_occurrence_dict[w]['w_sum'] = w_sum
    
    #open test file with latin_1 encoding
    #use translate() lib to remove punctuation 
    with codecs.open(testpath,encoding='latin_1',mode='r') as f:
        for j in f:
            j = j.split('\t')
            sentence = j[1].strip()
           
            sentence = sentence.translate(str.maketrans('','',string.punctuation))
            txt = sentence.split(' ')
            
            log_probabilities(lang_occurrence_dict, txt, langlist, j[0], j[1])
   
if __name__ == "__main__":
    main()

