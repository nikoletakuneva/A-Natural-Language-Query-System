# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements
import nltk


def add(lst, item):
    if (item not in lst):
        lst.insert(len(lst), item)


class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    # add code here
    global myList # list of tuples of word stems and their part-of-speech-category
    myList = []

    def add(self, stem, cat):
        tuple = (stem, cat)
        myList.append(tuple)

    def getAll(self, cat):
        words = []
        for t in myList:
            if t[1] == cat:
                add(words, t[0])
        return words


class FactBase:
    """stores unary and binary relational facts"""
    # add code here
    global unaryFacts
    unaryFacts = []
    global binaryFacts
    binaryFacts = []

    def addUnary(self, pred, e1):
        tuple = (pred, e1)
        add(unaryFacts, tuple)

    def addBinary(self, pred, e1, e2):
        tuple = (pred, e1, e2)
        add(binaryFacts, tuple)

    def queryUnary(self, pred, e1):
        tuple = (pred, e1)
        if (tuple in unaryFacts):
            return True
        else:
            return False

    def queryBinary(self, pred, e1, e2):
        tuple = (pred, e1, e2)
        if (tuple in binaryFacts):
            return True
        else:
            return False

import re
from nltk.corpus import brown

VB_list = [] #list of all the verb stems in the Brown corpus
VBZ_list = [] #list of all the 3s form verbs in the Brown corpus
for (w, tag) in nltk.corpus.brown.tagged_words():
    if (tag == "VB"):
        VB_list.append(w)
    elif (tag == "VBZ"):
        VBZ_list.append(w)

def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    # add code here
    stem = ""
    if (re.match("[a-z]*[^sxyzaeiou]s$", s) and not s.endswith("chs") and not s.endswith("shs")):
        stem = s[:-1]
    elif (re.match("[a-z]*[aeiou]ys$", s)):
        stem = s[:-1]
    elif (re.match("[a-z][a-z]*[^aeiou]ies$", s)):
        stem = s[:-3] + 'y'
    elif (re.match("[^aeiou]ies$", s)):
        stem = s[:-1]
    elif (re.match("[a-z]*(oes|xes|ches|shes|sses|zzes)$", s)):
        stem = s[:-2]
    elif (re.match("[a-z]*[^s]ses$", s)):
        stem = s[:-1]
    elif (re.match("has$", s)):
        stem = "have"
    elif (re.match("[a-z]*[^iosxz]es$", s) and not s.endswith("ches") and not s.endswith("shes")):
        stem = s[:-1]
    else:
        return ""

    if (s == "has" or s == "does" or s == "is"):
        return stem
    elif (stem in VB_list or stem in VBZ_list):
        return stem
    else:
        return ""


def add_proper_name(w, lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w, 'P')
        return ''
    else:
        return (w + " isn't a proper name")


def process_statement(lx, wlist, fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name(wlist[0], lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a', 'an']):
                lx.add(wlist[3], 'N')
                fb.addUnary('N_' + wlist[3], wlist[0])
            else:
                lx.add(wlist[2], 'A')
                fb.addUnary('A_' + wlist[2], wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add(stem, 'I')
                fb.addUnary('I_' + stem, wlist[0])
            else:
                msg = add_proper_name(wlist[2], lx)
                if (msg == ''):
                    lx.add(stem, 'T')
                    fb.addBinary('T_' + stem, wlist[0], wlist[2])
    return msg

# End of PART A.
