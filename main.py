import os
import matplotlib.pyplot as plotGraph
import logic as PreProcess
import util as Calculate
from tkinter import *

docList = {}

def preProcessData():
    """Preprocess the corpus taking all .txt files in directory
        and calls the preprocessing class for each of them"""
    files = [doc for doc in os.listdir() if (doc.endswith(
        '.txt') and (doc != 'DataStore.txt' and doc != 'temp.txt'))]
    for doc in files:
        docList[doc] = PreProcess.Preprocess(doc).trig


def storeCorpusData():
    """ Stores the preprocesed corpus in a text file
        to avoid the computational load of preprocessing
        every time"""
    trg = open('DataStore.txt', "w")
    trg.write(str(docList))
    trg.close()


def loadCorpusData():
    """Loads the preprocessed data"""
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
    """ Calls the preprocessing functions"""
    preProcessData()
    storeCorpusData()


def graphExecution():  # function that runs when we click the check button
    """ Gets the data from input boxes and preprocesses it
        adds the file to the corpus and finally graphs the
        plagiarism percentage in form of bar graph"""
    s = t.get("1.0", END)
    r = e1.get()
    r = r+'.txt'
    f = open(r, "w")
    f.write(s)
    f.close()
    inp = PreProcess.Preprocess(r).trig
    X = []
    Y = []
    doc_rank = Calculate.Logic(docList, inp).rank
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
