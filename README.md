# UKKC - Ukusanyaji-wa-Kiswahili-Kiingereza-Codeswitching (Swahili-English Code-Switching Corpus)  

  Huu ni ukusanyaji wa Tweets zinazojumuisha maneno ya Kiswahili na Kiingereza zote zawili kutoka Afrika Mashariki  
  > This is a collection of tweets which contain words of both Swahili and English from East Africa  

# Uumbaji wa UKKC (UKKC Creation)

  Ukusanyaji huu wametengeneza kwa kukusanya Tweets kutoka Afrika Mashariki. Tweets zimechuja kwa Lugha. Kama Twitter hawana kitambulisho cha Lugha ya Kiswahili, Tweets zote zimechuja kwa algorithm ya Machine Learning. Algorithm hii inatafuta lugha za Kiswahili na Kiingereza zote zawili Tweetini. Algorithm hii inapatikana pa CSidentify.py  
  >This corpus was created by collecting geographically tagged tweets from East Africa and filtering them by the language spoken. As Twitter does not have a Swahili language identifier, all tweets are filtered using a machine learning algorithm which searches for both English and Swahili in a given document (Tweet). This algorithm can be found in CSidentify.py  

  Uumbaji wa kisasa wanazojumuisha Tweets zilizochanga 10/2015 mpaka 11/2016.  
  >The current version of the corpus contains tweets collected at intervals between 10/2015 & 11/2016.  

  Mahali ya Tweets yanafuata:  
  >The coordinates used to collect the Tweets are as follows:  

  35.031750   **Magharibi**  
  >**Western Longitude**  
  -11.019555  **Kusini**  
  >**Southern Latitude**  
  41.513683   **Mashariki**  
  >**Eastern Longitude**  
  -1.826341   **Kaskazini**  
  >**Northern Latitude**  

# Language Identification

  The Language identification program is trained on 5 million token texts from Swahili and English blogs (10 million tokens total). The models are trained on character trigrams, and vote between whether the token in question is English or Swahili based upon multiple trigram association measures found in the NLTK package.

  For Identifying individual words, the Precision and Recall is as follows:

  Swahili:

    Precision = 0.84
    Recall    = 0.94

  English:

    Precision = 0.94
    Recall    = 0.82

# Swahili-English Code-Switching Identification

  The goal of this algorithm is to identify tweets such as the following:

    There's a breakout of kipindupindu hapa Lower Karen. Sasa ni Kuavoid kibandaski like it never existed.

  We label a tweet as containing Swahili English Code-Switching when English or Swahili are the matrix language, and there is a sequence of multiple words for the other language (Myers-Scotton 1997). We do not include non proper-nouns (Named Entities) as examples of Code-Switching.

  To detect code-switching within a tweet, we train a Logistic Regression model with tweets hand tagged as Code-Switched. For the algorithm, we extract various featuresxw:

  Language identification algorithm scores for each token,
  character trigrams,
  tokens,
  hashtags,
  mentions,
  geotags

  Features with a frequency count under a threshold of 10 were excluded, resulting in the use of around 22,000 features. The Logistical Regression algorithm was implemented using the Scikit package for Python3.

  For Identifying Code-Switching in Tweets, the Precision and Recall is as follows:


# Sources

  Myers-Scotton, Carol. Duelling languages: Grammatical structure in codeswitching. Oxford University Press, 1997.

###### Translations are my own. Corrections, Suggestions, and Comments are welcome!
