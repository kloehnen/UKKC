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
"""
__author__ = "Nick Kloehn"
__copyright__ = "Copyright 2015, Nick Kloehn"
__credits__ = []
__version__ = "1.0"
__maintainer__ = "Nick Kloehn"
__email__ = "See the author's website"
########################################################################
import nltk, numpy, random, re, sys, time
from happyfuntokenizing import *
from isLanguage import *
from nltk.probability import FreqDist
from scipy.sparse import lil_matrix
from sklearn.linear_model import LogisticRegression, Perceptron
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import precision_recall_fscore_support,accuracy_score
########################################################################
swaPath =("/Users/pokea/Documents/Work/UofA/"
  "Current/Dissertation/Productivity/Corpora/LanguageModels/Train/swa")
engPath = ("/Users/pokea/Documents/Work/UofA/"
  "Current/Dissertation/Productivity/Corpora/LanguageModels/Train/eng")
trainFile = ("/Users/pokea/Documents/Work/UofA/Current/Dissertation/"
  "Productivity/Corpora/Twitter/tweets.txt")
CodeSwitchOnly = True
#use_tokens = False
#use_langmod = False
EnglishOnly = False
KiswahiliOnly = False

########################################################################
#   Helper Functions
########################################################################

def parse_tweets(path):
  """Read through a file and extract tweets, their labels, and coordinates.
  Return a Dictionary where a tweet is a key, and (label,coors) the value."""
  parsed = {}
  f = re.split(r"\n", open(path).read())
  for line in f:
    try:
      label,tweet = re.split(r"\t+",line)
    except:
      continue
    parsed[tweet] = label
  return parsed

def getModelScores(tweet,LM):
  totalScore = np.array([])
  tweetChars = np.array(list(tweet.lower())) # get char list of tweet
  restChars = np.array([" " for _ in range(140-tweetChars.size)]) #remaining chars
  anchTweet = np.concatenate((tweetChars, restChars), axis=0) # anchor Tweet
  tweetGrams = char_ngrams("".join(anchTweet),3) #convert to string, get charngrams
  for t in tweetGrams:
    score = np.array(LM.scoreTrigram(t))
    totalScore = np.concatenate((totalScore,score), axis=0)
  return totalScore


def get_features(parsed,swaLM,engLM):
  """Take a dictionary of tweets, and the their coor,labels and produce
  training data Return X and Y matrix. Or if it's test, take the hashmap
  of tweets ...and, Return X-matrix."""
  y = np.array(parsed.values()) # get y labels
  # iter through tweets
  for tweet in iter(parsed.keys()):
    scoresLM1 = getModelScores(tweet,swaLM) # Get Model Scores
    scoresLM2 = getModelScores(tweet,engLM)
    tokenized_tweet = np.array(tok.tokenize(tweet)) # Tokenize Tweet
    #features = [char_ngrams(token,5) for token in tokenized_tweet]
    #features = flatten_list(features)
    #if use_tokens:
    #  features += tokenized_tweet
    #if use_langmod:
    #  features.append(Lm1.test(tweet))
    #  features.append(Lm2.test(tweet))
    #for feat in features:
    #  feats_dist[feat] += 1
    #  feats_dict[i] = features
  #feats_index = get_feat_index(feats_dist)
  #x = make_x(feats_index, feats_dict)
  #return x,numpy.array(y),feats_dict,feats_index

def char_ngrams(word, n, beg=' ', end=' '):
  """return list of char n-grams for a word (char ngrams, by convention)"""
  aword = beg * (n-1) + word + end * (n-1)
  return [aword[ch:ch+n] for ch in range(len(aword)-n+1)]

def flatten_list(list_of_lists):
  return [item for sublist in list_of_lists for item in sublist]

# Map from feature values to indices
def get_feat_index(feats_dist):
  feats_index = {}
  index = 0
  for f in feats_dist.keys():
    feats_index[f] = index
    index += 1
  return feats_index

# Generate x matrix
def make_x(feats_index, feats_dict):
  x = lil_matrix((len(feats_dict.keys()),len(feats_index.keys())))
  for i,feats in feats_dict.iteritems():
    for feature in feats:
      if feature in feats_index:
        x[i,feats_index[feature]] += 1
  return x

def compare(actual_y,predicted_y, pos):
  data = precision_recall_fscore_support(actual_y, predicted_y,
                                       average='macro', pos_label=pos)
  p,r,f1 = data[0], data[1], data[2]
  a = accuracy_score(actual_y, predicted_y)
  str = ("\n************************************************\n"
        "The Precision is", "{0:.4f}".format(p),".\n"
        "The Recall is", "{0:.4f}".format(r),".\n"
        "The F1 Score is", "{0:.4f}".format(f1),".\n"
        "The Accuracy Score is", "{0:.2f}".format(a*100),"%.\n"
        "************************************************\n")
  print(str)

########################################################################
#   Object Methods
########################################################################
class csClassifier:
  def __init__(self):
    """Initializes Object to classify whether CS occurs in a tweet. Trains
    lanuage models for each of the languages to be searched for, for future
    computation."""
    self.swaLM = LanguageModel(swaPath,swa=True)
    self.engLM = LanguageModel(engPath,swa=False)
    print("Done!")

  def train(self):
    get_features(parse_tweets(trainFile),self.swaLM,self.engLM)
    #x,y,feats_dict,feats_index = get_features(parsed,self.Lm1,self.Lm2)
    #self.feats_index = feats_index
    #if algorithm == 'LR':
    #  self.c = LogisticRegression().fit(x,y)
    #elif algorithm == 'NB':
    #  self.c = MultinomialNB().fit(x,y)
    #elif algorithm == 'PR':
    #  self.c = Perceptron().fit(x,y)
    #return self.c,self.feats_index

  def initial_test(self,test_file):
    parsed = parse_tweets(test_file)
    x,y,feats_dict2,feats_index2 = get_features(parsed,self.Lm1,self.Lm2)
    x2 = make_x(self.feats_index,feats_dict2)
    y2 = self.c.predict(x2)
    compare(y,y2,None)

  def test(self,parsed):
    x,y,feats_dict2,feats_index2 = get_features(parsed,self.Lm1,self.Lm2)
    x2 = make_x(self.feats_index,feats_dict2)
    y2 = self.c.predict(x2)
    return y2

C = csClassifier()
C.train()
