import os
import matplotlib.pyplot as plotGraph
from tkinter import *
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from queue import PriorityQueue
import re
         
def openFile(filename):
        f=open(filename,"r")
        orig=f.read().replace("\n"," ")
        orig = re.sub(r'[^\w\s]', '', orig)
        orig = re.sub(r'[0-9]+', '', orig)
        return word_tokenize(orig)

def clean(init_token):
        #lowercase
        tokens_o = [token.lower() for token in init_token]
        #stop word removal
        stop_words=set(stopwords.words('english'))
        #punctuation removal
        punctuations=['"','.','(',')',',','?',';',':',"''",'``']
        filtered_tokens = [w for w in tokens_o if not w in stop_words and not w in punctuations]
        return filtered_tokens

def makeTrig(clean_token):
        trigrams=[]
        for i in range(len(clean_token)-2):
            t=(clean_token[i],clean_token[i+1],clean_token[i+2])
            trigrams.append(t)
        return trigrams

def Preprocess(filename):
       trig = []
       init_token = openFile(filename)
       clean_token = clean(init_token)
       trig_list = makeTrig(clean_token)
       trig = trig_list
       return trig  

docList = {}

def preProcessData():
    files = [doc for doc in os.listdir() if (doc.endswith(
        '.txt') and (doc != 'DataStore.txt' and doc != 'temp.txt'))]
    for doc in files:
        tempTrig = []
        tempTrig = Preprocess(doc)
        docList[doc] = tempTrig


def storeCorpusData():
    trg = open('DataStore.txt', "w")
    trg.write(str(docList))
    trg.close()


def loadCorpusData():
    temp = open('DataStore.txt', 'r')
    s = temp.read()
    temp.close()
    docList = eval(s)
    print('a', docList)

master = Tk()
master.title("Plagiarism Checker")
master.config(bg="#FADA5E")  
Label(master, text="Enter file name", font=(
    "Helvetica", 12)).grid(row=0, column=1)

Label(master, text="Enter input text", font=(
    "Helvetica", 12)).grid(row=5, column=1)

master.geometry("750x780")
e1 = Entry(master) 

e1.grid(row=3, column=1, pady=15)


t = Text(master, width=80, height=35)
t.grid(row=6, column=1, padx=50, pady=10)


def PP():
    preProcessData()
    storeCorpusData()

def CalculateRank(corpus,inp):
        rank = PriorityQueue()
        for doc in corpus:    
            s = 0
            corp = corpus[doc]
            for tri in inp:
                if tri in corp:
                    s+=1
            rank.put((s/len(inp)*100,doc))
        return rank    


def graphExecution():  # function that runs when we click the check button
    s = t.get("1.0", END)
    r = e1.get()
    r = r+'.txt'
    f = open(r, "w")
    f.write(s)
    f.close()
    inp = Preprocess(r)
    X = []
    Y = []
    doc_rank = CalculateRank(docList, inp)
    for i in range(len(docList)):
        item = doc_rank.get()
        Y.append(item[0])
        X.append(item[1])

    plotGraph.bar(X, Y, width=0.5, align='center')
    plotGraph.xlabel("Doc Name")
    plotGraph.ylabel("% Similarity")
    plotGraph.title("Similarity Analaysis")
    plotGraph.xticks(rotation=90)
    plotGraph.tight_layout()
    plotGraph.show()

   
prep = Button(master, text='Process Data', bg='black',
              fg='white', width=24, command=PP) 
prep.grid(row=8, column=1, pady=10)

check = Button(master, text='Check Plagiarism', bg='black',
               fg='white', width=24, command=graphExecution)  
check.grid(row=12, column=1)

master.mainloop()
