#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This code produces a Corpus of Tweets containing Code Switching between English
 and Swahili. It does this by training a language model on Swahili, and another
 on English. The MLE value for each word in a tweet are the input to a machine
 learning algorithm that predicts the label of each tweet. Other features
 include charachter 5-grams, and tokens.

 Labels:
     0 English:
         Winners Win thank you Eden Hazard 3 more and we are champs...
     1 Swahili:
         Watoto Wa mama ntilie
     2 CodeSwitching:
         Herrera anajaribu stunts za Phelps
     3 Other:
         LOL! #MUFC http://t.co/rJiGqRqzg0

Written in Python 3.5.0
"""
__author__ = "Nick Kloehn"
__copyright__ = "Copyright 2015, Nick Kloehn"
__credits__ = []
__version__ = "1.0"
__maintainer__ = "Nick Kloehn"
__email__ = "See the author's website"
###############################################################################
from os import walk
from happyfuntokenizing import *
###############################################################################


class Corpus:
  def __init__(self,path,T):
    self.path = path
    self.T = T
    # Train Classifiers

  def create(self):
    # Open Twitter Data and filter
    infs = list()
    idSet = set()
    self.count = 0
    self.total = 0
    for (dpath,dnames,fs) in walk(self.path):
      infs.extend([self.path + '/' + f for f in fs if f.endswith('.txt')])
      for f in infs:
        with open(f) as infile:
          for line in infile:
            self.total += 1
            data = line.split('\t')
            if len(data) == 7:
              tweet = data[0]
              tweetID = data[4]
              # Make sure Tweets are unique
              if tweetID not in idSet:
                idSet.add(tweetID)
                self.count += 1
                # Tokenize Tweet
                tokenized_tweet = self.T.tokenize(tweet)
                # Filter using algorithm
                print(tokenized_tweet)

  def write(self,outdir):
    print(self.count)
    print(self.total)
    pass

def main():
  T = TweetTokenizer(preserve_case=True)
  C = Corpus(('/Users/pokea/Documents/Work/UofA/Current/Dissertation/'
              'Productivity/CS_Corpus/Unfiltered_Corpus'))
  C.create(T)
  C.write('s')

if __name__ == '__main__':
  
  main()



