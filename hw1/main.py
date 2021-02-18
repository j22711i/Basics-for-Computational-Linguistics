
#Juliana McCausland
#Ling 473
#Project 1

import os
import sys
import fnmatch
import re
import string
import math
import nltk
import nltk_tgrep as tgrep
from nltk import SExprTokenizer
from nltk.tree import ParentedTree



def file_cleanup(f):	
    content = []
    for i in f.readlines():

        #replacing new lines with white space
        i = re.sub(r"[\n\t]","",i)

        #.splitting i into a list
        lst = i.split(" ")

        #add to new list without the many '' found in lst
        for j in lst:
            if j != '':
                content.append(j)
    return content

def s_np_vp_count(fcontents, out_table):
#simple func to count the occurrences of each pattern for S, NP, and VP identified in this function
#each total count is added to dictionary (output table)
    
    count_s = 0

    s = '(S'
    stwo = '((S'
    count_stwo = fcontents.count(stwo)
    count_s = fcontents.count(s)
    total_s = count_s + count_stwo
    out_table['Sentence'] += total_s

    count_np = 0
    np = '(NP'
    count_np = fcontents.count(np)
    out_table['Noun Phrase'] += count_np

    count_vp = 0
    vp = '(VP'
    count_vp = fcontents.count(vp)
    out_table['Verb Phrase'] += count_vp


    return out_table['Sentence'], out_table['Noun Phrase'], out_table['Verb Phrase']

def access_files(cpath):
#get directory list of files
    return os.listdir(cpath)

def dvp_count(ptrees, out_table):
#ditransitive verb phrase count - using parented trees 

    #assigning ditransitive verb tree structure/pattern to find_dvp -- will be used to search ptrees 
    #('<' signifies immediate dominance and $ signifies a sibling relationship)
    find_dvp = 'VP < (NP $ NP)'
    
    #tree grep function to search the parented trees for matching parameters
    tgrep_dvp = tgrep.tgrep_nodes(ptrees, find_dvp)

    #now searching within the matching trees for those with the correct number of nodes
    final_dvp_lst = []
    for i in tgrep_dvp:
        if len(i) == 3:
            final_dvp_lst.append(i)
    final_value = len(final_dvp_lst)
    out_table['Ditransitive Verb Phrase'] += final_value
    
    #return new dictionary value for ditransitive vp 
    return out_table['Ditransitive Verb Phrase']

def ivp_count(ptrees, out_table):
#intransitive verb phrase count
#ivp_count operates the same way as dvp_count, but searches for only 'VP' with the structure of an intransitive vp
    
    find_ivp = 'VP'
    tgrep_ivp = tgrep.tgrep_nodes(ptrees, find_ivp)
    final_ivp_lst = []
    for i in tgrep_ivp:
        if len(list(i.subtrees())) == 1:
            final_ivp_lst.append(i)
    final_ivp_val = len(final_ivp_lst)
    out_table['Intransitive Verb Phrase'] += final_ivp_val
    
    #return dictionary value for intransitive vp
    return out_table['Intransitive Verb Phrase']


def main():
    #create a dictionary for the output values
    out_table = {'Sentence':0, 'Noun Phrase':0, 'Verb Phrase':0, 'Ditransitive Verb Phrase':0, 'Intransitive Verb Phrase':0}

    cpath = "/corpora/LDC/LDC99T42/RAW/parsed/prd/wsj/14"

    #OPEN/READ part 1: (this applies to counting S, NP, and VP)
    for path, directories, files in os.walk(cpath):
        for fn in fnmatch.filter(files, '*prd'):
            with open(os.path.join(path, fn)):
                fcontents = file_cleanup(open(path+'/'+fn))
                s_np_vp_count(fcontents, out_table)
    #OPEN/READ part 2: (this applies to counting Ditransitive and Intransitive VPs)
    if os.path.isdir(cpath):
        files = access_files(cpath)
        for fi in files:
            with open(cpath+'/'+fi, 'r') as f:
                #s-expression tokenizer to create substrings of parenthesized expressions -- using this to create parented trees
                new = SExprTokenizer(strict=False).tokenize(''.join(map(str.strip,f.readlines())))
                ptrees = [ParentedTree.fromstring(s) for s in new]
                
            #iterate through trees while calling ditransitive and intransitive functions
            for i in ptrees:
                dvp_count(i, out_table)
                ivp_count(i, out_table)
        #print the key and value pairs from dictionary (the output table)
        for num in out_table:
            print('{}\t{}'.format(num,out_table[num]))
           # print(out_table)



if __name__ == '__main__':
    main()
