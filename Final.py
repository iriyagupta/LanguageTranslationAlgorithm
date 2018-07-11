import os
import sys
import codecs #for encoding the hindi/non-english data
import re #for the data to search for expressions


#lcs algo to find longest common string
def lcs(a, b):
    lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
    # row 0 and column 0 are initialized to 0 already
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i+1][j+1] = lengths[i][j] + 1
            else:
                lengths[i+1][j+1] = \
                    max(lengths[i+1][j], lengths[i][j+1])
    # read the substring out from the matrix
    result = ""
    x, y = len(a), len(b)
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x-1][y]:
            x -= 1
        elif lengths[x][y] == lengths[x][y-1]:
            y -= 1
        else:
            assert a[x-1] == b[y-1]
            result = a[x-1] + result
            x -= 1
            y -= 1
    return result

#opening the dictionary
newDict={}
Store={}
fileName=codecs.open("riya\\tester.txt",encoding="utf-8")
lines = fileName.read()
a=lines.split("\n")
for i in a:
    x= i.split(" ")
    try:
        tmp=""
        temp=[]
        temp.append(x[0])
        temp.append(x[1])
        tmp=" ".join(temp)
        Store[x[0]]=1
        newDict[tmp]=x[2]
    except IndexError as err:
        kk=0
#print Store
#print newDict

#stopword file
stopword= codecs.open('riya\\hindistop.txt', encoding='utf-8')
txt = stopword.read()
lines= txt.split('\n')
sep=" "
stopwords=sep.join(lines)
#print stopwords
stopword.close()

#for the printing of words in the list
fileToAppend=codecs.open("riya\\translatedfile2011.txt","w",encoding="utf-8")
second=codecs.open('riya\\hi.topics.126-175.2011.txt',encoding='utf-8')
text=second.read()
arrays= text.split('\n')
#print arrays
count=0 #counter for words in vocab
score=0 #counter for words out of vocab
finalId=125 #initial id
for i in arrays:
    array=[]
    if(re.search("<title>",i)): #searches if title tag is present or not
       finalId +=1 #creates the id of the query
       match=re.match(r"^\<.*\>(.*)\<",i) #matching and selecting the 1st part of the grp created i.e title
       line=match.group(1) #prints the title part of our query
       print line
       fileToAppend.write(str(finalId))
       fileToAppend.write(" ")
       fileToAppend.write(line)
       fileToAppend.write(" ")
       words = line.split(" ")
       #print words
       for j in words:   #for creating an array to store words not prrent in the stopword list
           if (not re.search(j,stopwords)):
               array.append(j)  #array created
       #print array
       
       for k in array: #if kis present in the key
           f=0
           if k in Store.keys():
               f=1
               print k
               for group in newDict.keys():
                   newWords=group.split(" ")
                   if (k==newWords[0]):
                       a=newWords[1]
                       print a
                       fileToAppend.write(a)
                       fileToAppend.write(" ")
                       count+=1
           elif k not in Store.keys():   #if k is not present in the list
               empty=""
               maxsc=0.0
               for key in Store.keys():
                   emptyS=""
                   emptyS=lcs(k,key)
                   scr=0
                   scr=float(len(emptyS))/max(len(k),len(key))
                   if(scr>maxsc):
                       maxsc=scr
                       empty=key
                   #print emptyS
               if (maxsc>0.75):
                   f=1
                   print key
                   for group in newDict.keys():
                       newWords=group.split(" ")
                       if key==newWords[0]:
                           print newWords[1]
                           fileToAppend.write(newWords[1])
                           fileToAppend.write(" ")
                           count+=1
           if f==0:   #if not at all present , print hindi word
                print k
                fileToAppend.write(k)
                fileToAppend.write(" ")
                score+=1
                
       fileToAppend.write("\n")
print "Total Vocab words: ",count
fileToAppend.write("Total Vocab words: ")
fileToAppend.write(str(count))
fileToAppend.write("\n")
print "Words out of vocab: ",score
fileToAppend.write("Total Vocab words: ")
fileToAppend.write(str(score))
fileToAppend.write("\n")

