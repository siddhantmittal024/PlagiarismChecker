from queue import PriorityQueue

class Logic:
    '''
     This class calculates similarity between all the documents present in the dataset with the doc to be checked
     Rank will contain number of trigram that matches per unit length for a given doc
     Doc with higher priority will have more similarity than a doc with lower priority
    '''
    rank = PriorityQueue()
    """ Priority queue with percentage plagiarism and doc name"""
    def __init__(self,corpus,inp):
        """
          Run a loop through all the documents, for each document if there is a trigram match increment the count
          When all trigrams matched add its value to the queue as count per unit length
        """
        for doc in corpus:    
            s = 0
            corp = corpus[doc]
            for tri in inp:
                if tri in corp:
                    s+=1
            self.rank.put((s/len(inp)*100,doc))