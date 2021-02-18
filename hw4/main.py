

#Juliana McCausland
#Ling 473
#Project 4

from collections import defaultdict
import sys
import io
import os


#nucleotide_A = 'A'
#nucleotide_T = 'T'
#nucleotide_G = 'G'
#nucleotide_C = 'C'

class trieNode:

    def __init__(self, char, end):
        
        self.children = [None] * 4
        self.char = char
        self.end = end
        
    def insrt(self, nucleotide):
    #insert children nodes corresponding to each nucleotide (A, C, G, or T)
        if nucleotide.char == 'A':
            self.children[0] = nucleotide
        elif nucleotide.char == 'C':
            self.children[1] = nucleotide
        elif nucleotide.char == 'G':
            self.children[2] = nucleotide
        elif nucleotide.char == 'T':
            self.children[3] = nucleotide

class Trie:
    def __init__(self):
        self.root = self.get_trieNode()
        
    def get_trieNode(self):
        return trieNode("root", False)

    def get(self):
        return self.root

    def insrt(self, strng):
    #each time a character matches A,C,T,or G, we insert children when necessary through the insert function in the trieNode class
        root = self.root
        for i in strng:
            if i == 'A':
                if root.children[0] == None:
                    root.insrt(trieNode(i,False))
                root = root.children[0]
            elif i == 'C':
                if root.children[1] == None:
                    root.insrt(trieNode(i,False))
                root = root.children[1]
            elif i == 'G':
                if root.children[2] == None:
                    root.insrt(trieNode(i,False))
                root = root.children[2]
            elif i == 'T':
                if root.children[3] == None:
                    root.insrt(trieNode(i,False))
                root = root.children[3]
        root.end = True #reached last character -- finished


def extra_cred(strng, xtra):
#extra credit
    with open('ExtraCredit','w') as w:
        for strng in xtra:
            w.write(strng+'\n')
            for k in xtra[strng]:
                w.write(k +'\n')

def main():

    #dictionary for extra credit items
    xtra = {}

    tr = Trie()
    
    with open('/opt/dropbox/19-20/473/project4/targets', 'rb') as f:
        for i in f:
            tr.insrt(i.strip().upper()) #run target file through trie to leave us with desired strings 
    
    #sys.argv[1] is individual file from h19-GRCh37 directory
    fi = sys.argv[1]
    
    #printing file for output before printing desired contents of each file    
    fi_print = os.path.join('/opt/dropbox/19-20/473/project4/hg19-GRCh37/', fi)
    print(fi_print)
        
         
    with open(fi, 'rb') as f:  
        txt = f.read().upper()  
        i = 0
        
        #while i and j are less than length of file -- search file for matches with target strings    
        while i < len(txt):
            j = i
            root = tr.get()
            while j < len(txt):
                curr = txt[j]
                if curr == 'A' and root.children[0] != None:
                    root = root.children[0]
                elif curr == 'C' and root.children[1] != None:
                    root = root.children[1]
                elif curr == 'G' and root.children[2] != None:
                    root = root.children[2]
                elif curr == 'T' and root.children[3] != None:
                    root = root.children[3]
                elif root.end == True:
                    
                    strng = txt[i:j]
                    print("\t"+ str(format(i, '08X')) +"\t" + strng)
                    
                    #regroup items for extra credit format    
                    if strng not in xtra:
                        xtra[strng] = []
                    xtra[strng].append('\t'+str(format(i, '08X'))+'\t'+fi)
                    break
                else:
                    break
                j += 1
            i += 1
    
    extra_cred(strng, xtra)

if __name__ == "__main__":
    main()

