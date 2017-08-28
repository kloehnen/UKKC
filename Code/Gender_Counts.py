#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Count the number of nouns in Swahili, and choose how many exist for each gender. 
If possible, see how many are derived from Verbs or other parts of speech.
"""
__author__ = "Nick Kloehn"
__copyright__ = "Copyright 2015, Nick Kloehn"
__credits__ = []
__version__ = "1.0"
__maintainer__ = "Nick Kloehn"
__email__ = "See the author's website"
########################################################################
import os,re,xml.etree.ElementTree as ET
from os import walk
########################################################################

nTags = [['1/2-SG'],
            ['1/2-PL'],
            ['3/4-SG'],
            ['3/4-PL'],
            ['5/6-SG','5a/6-SG'],
            ['5/6-PL','5a/6-PL','9/6-0-PL','11/6-PL','6-PL'],
            ['7/8-SG'],
            ['7/8-PL'],
            ['9/10-0-SG','9/10-NI-SG','9/6-0-SG','9/10-SG'],
            ['9/10-0-PL','9/10-NI-PL','11/10-PL','3/10-PL','9/10-PL'],
            ['11/6-SG','11/10-SG','11-SG'],
            ['15-SG'],
            ['16-SG','LOC-16'],
            ['17-SG','LOC-17'],
            ['18-SG','LOC-18']]

vTags = [['1/2-SG-SP','1/2-SG1-S','1/2-SG2-SP','1/2-SG3-SP','SG3-SP'],
            ['1/2-PL1-SP','1/2-PL2-S','1/2-PL3-SP','PL3-SP'],
            ['3/4-SG-SP'],
            ['3/4-PL-SP'],
            ['5/6-SG-SP'],
            ['5/6-PL-SP'],
            ['7/8-SG-SP'],
            ['7/8-PL-SP'],
            ['9/10-SG-SP'],
            ['9/10-PL-SP'],
            ['11-SG-SP'],
            ['15-SG-SP'],
            ['16-SG-SP'],
            ['17-SG-SP'],
            ['18-SG-SP']]

def matchTags(features,C,nouns):
    # match the noun class feature to its class
    if features != None:
        if nouns:
            tags = nTags
        else:
            tags = vTags
        for idx in range(len(tags)):
            for tag in nTags[idx]:
                if tag in features:
                    C.addtoNclass(idx)
                    return True

def evaluateNgram(nGramTuple,C):
    match = False
    if str(nGramTuple[1]).lower().startswith("a"):
        match = matchTags(nGramTuple[0],C,nouns=True)
    elif str(nGramTuple[1]).lower().startswith("v"):
        match = matchTags(nGramTuple[0],C,nouns=False)
    elif str(nGramTuple[1]).lower().startswith("gen-con"):
        match = matchTags(nGramTuple[0],C,nouns=True)
    return match

class FileRead:

    def __init__(self,counter,dev=True):
        self.path = os.getcwd()
        self.C = counter
        self.in_files = []
        if not dev:
            self.in_path = '/proj/csc/ling/kielipankki/hcs'
        else:
            self.in_path = ('/Users/pokea/Documents/Work/'
                'UofA/Current/Dissertation/Productivity/'
                'HSC/Past/articles')

    def walk(self):
        # Walk through XML files...
        for (dirpath, dirnames, in_filenames) in walk(self.in_path):
            self.in_files.extend([dirpath + '/' + f for f in in_filenames])
        words_seen = 0
        for f in self.in_files:
            if f.endswith(".xml"):
                try:
                    # Parse them using etree
                    root = ET.parse(f).getroot()
                    rootlist = list(root.iter('w'))
                    print("Parsed "+f)
                    size = len(rootlist)
                    # Get total count of tokens based upon size of tree
                    self.C.addtoWordsSeen(size)
                    for idx in range(size):
                        aDict = rootlist[idx].attrib
                        if 'type' in aDict.keys():
                            # count adjectives
                            if str(aDict['type']).lower().startswith("a"):
                                self.C.addtoNadj()
                            # count verbs
                            if str(aDict['type']).lower().startswith("v"):
                                self.C.addtoNverbs()
                            # if it's a noun..
                            if aDict['type'] == 'N':
                              # if the token marks agreement..
                                if 'msd' in aDict.keys():
                                    propFeats = aDict['msd']
                                    # Count the derived ones
                                    if 'DER:adj' in propFeats:
                                        self.C.addDadj()
                                    elif 'DER:verb' in propFeats:
                                        self.C.addDverb()
                                    # match the tag in the Counter object
                                    madeMatch = matchTags(propFeats,self.C,nouns=True)
                            # if it's a proper noun...
                            elif aDict['type'] == 'PROPNAME':
                                # Determine whether it has agrFeats
                                propFeats = None
                                if 'msd' in aDict.keys():
                                    propFeats = aDict['msd']
                                # make it an objext to estimate its gender
                                P = PropName((propFeats,aDict['type']),self.C)
                                # add the type and agreement features of next 2 tokens
                                iList = [1,2]
                                for jdx in iList:
                                    try:
                                        agrFeats,typeFeats = None,None
                                        nDict = rootlist[idx+jdx].attrib
                                        if 'msd' in nDict.keys():
                                            agrFeats = nDict['msd']
                                        if 'type' in nDict.keys():
                                            typeFeats = nDict['type']
                                        P.addNgram((agrFeats,typeFeats),jdx)
                                    except:
                                        continue
                                P.getTag()
                except:
                    print("Couldn't Parse "+f)

class PropName:

    def __init__(self,pnTuple,C):
        self.C = C
        self.pnTuple = pnTuple
        self.plus1Tuple = None
        self.plus2Tuple = None

    def addNgram(self,ngramTuple,offset):
        self.offset = offset
        if self.offset == 1:
            self.plus1Tuple= ngramTuple
        elif self.offset == 2:
            self.plus2Tuple = ngramTuple

    def getTag(self):
        match = evaluateNgram(self.plus1Tuple,self.C)
        if match == False:
            if self.plus2Tuple != None:
                match = evaluateNgram(self.plus2Tuple,self.C)
        if match == False:
            self.C.addtoNnouns()


class Counter:

    def __init__(self):
        self.Nnouns = 0
        self.Nverbs = 0
        self.Nadj = 0
        self.Dadj = 0
        self.Dverb = 0
        self.wordsSeen = 0
        self.Nclasses = list([0]) * 15

    def addtoNclass(self,classIndex):
        self.Nclasses[classIndex] += 1

    def addtoNnouns(self):
        self.Nverbs += 1

    def addtoNverbs(self):
        self.Nverbs += 1

    def addtoNadj(self):
        self.Nadj += 1

    def addDadj(self):
        self.Dadj += 1

    def addDverb(self):
        self.Dverb += 1

    def addtoWordsSeen(self,n):
        self.wordsSeen += n

    def getNclass(self):
        return self.Nclasses

    def getNproNoagr(self):
        return self.Nnouns

    def getNadj(self):
        return self.Nadj

    def getDadj(self):
        return self.Dadj

    def getDverb(self):
        return self.Dverb

    def getNnouns(self):
        return sum(self.Nclasses)

    def getNverbs(self):
        return self.Nverbs

    def getWordsSeen(self):
        return self.wordsSeen

class Writer:

    def __init__(self,counter):
        self.C = counter

    def write(self):

        print("Number of total verbs\t"+str(self.C.getNverbs()))
        print("Number of total adjectives\t"+str(self.C.getNadj()))
        print("Number total nouns\t"+str(self.C.getNnouns()))
        print("Number for each noun class\t"+str(self.C.getNclass()))
        print("Number of pronouns with no agreement\t"+str(self.C.getNproNoagr()))
        print("Number of nouns derived from adjectives\t"+str(self.C.getDadj()))
        print("Number of nouns derived from verbs\t"+str(self.C.getDverb()))
        print("Number of total tokens seen\t"+str(self.C.getWordsSeen()))

def main():
    tagset = []
    c = Counter()
    FileRead(c).walk()
    Writer(c).write()

if __name__ == '__main__':
    main()
