

# Juliana McCausland
# Ling 473
# Project 2

import os
import sys
import re

def access_files(cpath):
#get directory list of files
    return os.listdir(cpath)

def file_cleanup(fi):
   
    with open(fi, 'r') as f:
        newtxt = ''.join(f.readlines())
    #removing all SGML tags
    sgml = '<.*?>'
    newtxt = re.sub(sgml, '', newtxt)

    #remove unwanted chars and replace with space
    newtxt = re.sub(r'[^A-Za-z\']', ' ', newtxt)

    #strip the unwanted apostrophes
    bg_apost = ' \'*' 
    newtxt = re.sub(bg_apost,' ', newtxt)
    end_apost = '\'* ' 
    newtxt = re.sub(end_apost, ' ', newtxt).lower()

    #split newtxt into a list called cleanfile 
    cleanfile = newtxt.split()
    return cleanfile


def main():
    cpath = '/corpora/LDC/LDC02T31/nyt/2000'
    files = access_files(cpath)
    
    #iterate through each file, calling file_cleanup function and concatenate returned files to list cleanf
    cleanf = []
    for fi in files:
        cleanf += file_cleanup(os.path.join(cpath, fi))

    #add words to new dictionary (wrd_dictionary) and their corresponding counts
    #works by checking if word already exists in dict, and incrementing +1 for each occurence beyond ininitial occurrence 
    wrd_dictionary = {}
    for word in cleanf:
        if word not in wrd_dictionary: 
            wrd_dictionary[word] = 1
        else:
            wrd_dictionary[word] += 1

    #new list which will be used as the final unigram (output) 
    sortd_unigram = []

    #appendign each value-key pair from dictionary to unigram list
    for j,m in wrd_dictionary.items():
        sortd_unigram.append((m,j))

    #sort unigram --> reverse = True enables descending order  
    sortd_unigram = sorted(sortd_unigram, reverse = True)

    for i in sortd_unigram:
        print('%s\t%d' %(i[1], i[0]))

if __name__ == '__main__':
    main()             
