import os
import matplotlib.pyplot as plt
import ProcessData as pp
import SimilarityCalculator as cs
from tkinter import *

l = {}

def ppcorpus():
    """Preprocess the corpus taking all .txt files in directory
        and calls the preprocessing class for each of them"""
    files = [doc for doc in os.listdir() if (doc.endswith(
        '.txt') and (doc != 'store.txt' and doc != 'temp.txt'))]
    for doc in files:
        l[doc] = pp.Preprocess(doc).trig


def storeCorpus():
    """ Stores the preprocesed corpus in a text file
        to avoid the computational load of preprocessing
        every time"""
    target = open('store.txt', "w")
    target.write(str(l))
    target.close()


def loadCorpus():
    """Loads the preprocessed data"""
    ter = open('store.txt', 'r')
    s = ter.read()
    ter.close()
    l = eval(s)
    print('a', l)

master = Tk()
master.title("Plagiarism Checker")
master.config(bg="#FADA5E")  # title of the window
Label(master, text="Enter file name", font=(
    "Helvetica", 12)).grid(row=0, column=1)

Label(master, text="Enter input text", font=(
    "Helvetica", 12)).grid(row=5, column=1)

master.geometry("750x780")
e1 = Entry(master)  # text field to input file name

e1.grid(row=3, column=1, pady=15)

# text field to input text to be checked
t = Text(master, width=80, height=35)
t.grid(row=6, column=1, padx=50, pady=10)


def Prepro():
    """ Calls the preprocessing functions"""
    ppcorpus()
    storeCorpus()


def helloCallBack():  # function that runs when we click the check button
    """ Gets the data from input boxes and preprocesses it
        adds the file to the corpus and finally graphs the
        plagiarism percentage in form of bar graph"""
    s = t.get("1.0", END)
    r = e1.get()
    r = r+'.txt'
    f = open(r, "w")
    f.write(s)
    f.close()
    inp = pp.Preprocess(r).trig
    X = []
    Y = []
    doc_rank = cs.CalcSim(l, inp).doc_rank
    for i in range(len(l)):
        item = doc_rank.get()
        Y.append(item[0])
        X.append(item[1])
    # graph the similarity

    plt.bar(X, Y, width=0.5, align='center')
    plt.xlabel("Doc Name")
    plt.ylabel("% Similarity")
    plt.title("Similarity Analaysis")
    plt.xticks(rotation=90)
    plt.tight_layout()
    #plt.grid()
    plt.show()
    # master.destroy()
    '''Output Frame'''


prep = Button(master, text='Process Data', bg='black',
              fg='white', width=24, command=Prepro)  # check button
prep.grid(row=8, column=1, pady=10)

check = Button(master, text='Check Plagiarism', bg='black',
               fg='white', width=24, command=helloCallBack)  # check button
check.grid(row=12, column=1)

master.mainloop()
