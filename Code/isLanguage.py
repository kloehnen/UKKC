from nltk.collocations import TrigramCollocationFinder
from nltk.collocations import TrigramAssocMeasures
import string,nltk,re,math, numpy as np

trigram_measures = TrigramAssocMeasures()
translate_table = dict((ord(char), None) for char in string.punctuation)

def reportPR(score1,score2,total1,total2):
  print(score1)
  print(score2)
  print(total1)
  print(total2)
  false1 = total1 - score1
  false2 = total2 - score2
  # Precision = True Positives / True Positives + False Positives
  P1 = float(score1) / (false2 + score1)
  P2 = float(score2) / (false1 + score2)
  # Recall = True Positives / True Positives + False Negatives
  R1 = score1 / (false1 + score1)
  R2 = score2 / (false2+ score2)
  print("For Swahili:\n\tPrecision = " + str(P1) + "\n\Recall = " + str(R1))
  print("For English:\n\tPrecision = " + str(P2) + "\n\Recall = " + str(R2))

def readFile(path):
  all_words = []
  with open(path, encoding="ISO-8859-1") as file:
    for line in file:
      all_words += [token for token in re.split(r"\s+","".join(filterLine(line)))]
  all_words = iter([token for token in all_words if token]) # remove weird empty strings
  return all_words

def filterLine(line):
  if len(line) > 1:
    line = re.sub(r"\d","", line) # remove digits
    line = line.translate(translate_table) # remove punctuation
    line = "".join(ch.lower() for ch in line) # collapse case
    return line
  else:
    return ""

def addMeasures(*lists):
  return map(sum, zip(*lists))

def train_language(path,swa):
  words_all = list()
  totalTokens = 0
  maxTokens = 4955000
  # reading the file in unicode format using codecs library
  with open(path, encoding="ISO-8859-1") as file:
    for line in file:
      if swa:
        line = re.split(r"\t+",line)[4]
      # extracting the text sentence from each line
      for token in iter(re.split(r"\s+",filterLine(line))):
        if totalTokens != maxTokens:
          if token:
            words_all.append(token)
            words_all.append("  ")
            totalTokens += 1
  words_all = list("".join(words_all))
  #print("Trained the model with %d total tokens" % (totalTokens))
  return TrigramCollocationFinder.from_words(words_all),totalTokens

def char_ngrams(word, n, beg=' ', end=' '):
  """return list of char n-grams for a word (char ngrams, by convention)"""
  aword = beg * (n-1) + word + end * (n-1)
  return [aword[ch:ch+n] for ch in range(len(aword) - n + 1)]

class LanguageModel:
  def __init__(self,path,swa):
    self.model, self.total = train_language(path,swa)

  def getTotal(self):
    return self.total

  def getScore(self,token):
    tokenNgrams = char_ngrams(token,3)
    overall = []
    for trigram in tokenNgrams:
      score = []
      ixx,xix,xxi = trigram
      score.append(self.model.score_ngram(trigram_measures.chi_sq,ixx,xix,xxi))
      score.append(self.model.score_ngram(trigram_measures.jaccard,ixx,xix,xxi))
      score.append(self.model.score_ngram(trigram_measures.likelihood_ratio,ixx,xix,xxi))
      score.append(self.model.score_ngram(trigram_measures.pmi,ixx,xix,xxi))
      score.append(self.model.score_ngram(trigram_measures.poisson_stirling,ixx,xix,xxi))
      score.append(self.model.score_ngram(trigram_measures.student_t,ixx,xix,xxi))
      for idx in range(len(score)):
        if not score[idx]:
          score[idx] = 0
      overall.append(score)
      seq = np.sum(np.array(overall),axis=0)
    if seq.size != 6:
      return np.array([])
    return seq

class PRTest:
  def __init__(self,L1,L2,path):
    self.ML1 = L1
    self.ML2 = L2
    self.test = readFile(path)

  def getTotals(self):
    self.total = 0
    self.score = 0
    for token in self.test:
      vote1 = 0
      vote2 = 0
      score1 = self.ML1.getScore(token)
      score2 = self.ML2.getScore(token)
      if score1.size == score2.size:
        for idx in range(score1.size):
          current1 = score1[idx]
          current2 = score2[idx]
          if current1 > current2:
            vote1 += 1
          elif current2 > current1:
            vote2 += 1
          else: continue
      self.total += 1
      if vote1 > vote2:
        self.score += 1
      else:
        pass
        print("missed %s" % (token))
    return (self.score,self.total)

Swa = LanguageModel(path="/Users/pokea/Desktop/swa",swa=True)
Eng = LanguageModel(path="/Users/pokea/Desktop/eng",swa=False)

SwaTotal = Swa.getTotal()
EngTotal = Eng.getTotal()

P1 = PRTest(Swa,Eng,'/Users/pokea/Desktop/Swa_Test')
P2 = PRTest(Eng,Swa,'/Users/pokea/Desktop/Eng_Test')

score1,total1 = P1.getTotals()
score2,total2 = P2.getTotals()

reportPR(score1,score2,total1,total2)
