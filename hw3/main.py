

#Juliana McCausland
#Ling 473
#Project 3

import sys
import site
import io
import codecs

V1 = u"\u0E40\u0E41\u0E42\u0E43\u0E44"
C1 = u"\u0E01\u0E02\u0E03\u0E04\u0E05\u0E06\u0E07\u0E08\u0E09\u0E0A\u0E0B\u0E0C\u0E0D\u0E0E\u0E0F" \
     + u"\u0E10\u0E11\u0E12\u0E13\u0E14\u0E15\u0E16\u0E17\u0E18\u0E19\u0E1A\u0E1B\u0E1C\u0E1D\u0E1E\u0E1F" \
     + u"\u0E20\u0E21\u0E22\u0E23\u0E24\u0E25\u0E26\u0E27\u0E28\u0E29\u0E2A\u0E2B\u0E2C\u0E2D\u0E2E"
C2 = u"\u0E23\u0E25\u0E27\u0E19\u0E21"
V2 = u"\u0E34\u0E35\u0E36\u0E37\u0E38\u0E39\u0E31\u0E47"
T  = u"\u0E48\u0E49\u0E4A\u0E4B"
V3 = u"\u0E32\u0E2D\u0E22\u0E27"
C3 = u"\u0E07\u0E19\u0E21\u0E14\u0E1A\u0E01\u0E22\u0E27"

    

def main():

    f = codecs.open("./fsm-input.utf8.txt", encoding = 'utf-8').readlines()
    
    #creating output file
    out = codecs.open("./jumc1469.html", encoding = 'utf-8', mode = 'w')
    out.write(u"<html><meta http-equiv='Content-Type' content='text/html; charset=UTF-8' /><body>")
    
    for i in f:
        I = i[:-1]

        #use enumerate() function to assign indx values to chars in I -- to keep track 
        I_enum = enumerate(I)

        state = 0
        txt = ''

        #dictionary for keeping track of positions for states 7, 8, and 9
        w_dict = {}
        idx = 1
        w_dict[idx] = [{'idx1':0},{'idx2':0}]
        
        #here lies the FSM..based on the specifications in the project description
        for i, j in I_enum:
            
            if state == 0:  #state 0 accepts V1 and C1
                if j in V1: #V1 transitions to state 1, C1 transitions to state 2
                    state = 1
                elif j in C1:
                    state = 2
            elif state == 1: #state 1 accepts only C1
                if j in C1:
                    state = 2
            elif state == 2: #state 2 accepts C2, V2, T, V3, C3, V1
                if j in C2:
                    state = 3
                elif j in V2:
                    state = 4
                elif j in T:
                    state = 5
                elif j in V3:
                    state = 6
                elif j in C3:
                    state = 9
                elif j in V1:
                    if i == len(I)-1:
                        break
                    else:
                        state = 7
                elif j in C1:
                    if i == len(I)-1:
                        break
            elif state == 3: #state 3 accepts V2, T, V3, C3
                if j in V2:
                    state = 4
                elif j in T:
                    state = 5
                elif j in V3:
                    state = 6
                elif j in C3:
                    state = 9
            elif state == 4: #state 4 accepts T, V3, C3, V1, C1
                if j in T:
                    state = 5
                elif j in V3:
                    state = 6
                elif j in C3:
                    state = 9
                elif j in V1:
                    if i == len(I)-1:
                        break
                    else:
                        state = 7
                elif j in C1:
                    if i == len(I)-1:
                        break
                    else:
                        state = 8   
            elif state == 5: #state 5 accepts V3, C3, V1, C1 
                if j in V3:
                    state = 6
                elif j in C3:
                    state = 9
                elif j in V1:
                    if i == len(I)-1:
                        break
                    else:
                        state = 7
                elif j in C1:
                    if i == len(I)-1:
                        break
                    else:
                        state = 8
            elif state == 6: #state 6 accepts C3, V1, C1
                if j in C3:
                    state = 9
                elif j in V1:
                    if i == len(I)-1:
                        break
                    else:
                        state = 7
                elif j in C1:
                    if i == len(I)-1:
                        break
                    else:
                        state = 8

            #states 7, 8, and 9: syllable break detected
            #if state 7 or 8: break before previous character and transition (7 --> 1), (8 --> 2)
            #if state 9: break and transition --> 0
            #using dictionary indexes to track previous chars and insterting space after previous char
            if state == 7 or state == 8 or state == 9:
                
                w_dict[idx][1]["idx2"] = i-1
                if state == 9:
                    w_dict[idx+1] = [{"idx1":i+1},{"idx2":0}]
                else:
                    w_dict[idx+1] = [{"idx1":i},{"idx2":0}]
                idx_from = w_dict[idx][0]["idx1"]
                idx_to = w_dict[idx][1]["idx2"]
                

                if state == 9:
                    txt = txt + I[idx_from:idx_to+2]+u" "

                else:
                    txt = txt + I[idx_from:idx_to+1]+u" "
                idx += 1

                if state == 8:
                    state = 2
                elif state == 7:
                    state = 1
                elif state == 9:
                    state = 0


        #if there is a missing char at end of line -- add to txt 
        if w_dict[idx][0]["idx1"] < len(I):
            txt = txt + I[w_dict[idx][0]["idx1"]:len(I)]

        txt = txt.strip()

       #write txt to output file
        out.write(txt + u"<br />\n")   
    out.write(u"</body></html>")

    #close output 
    out.close()
           
        
if __name__=="__main__":
    main()
