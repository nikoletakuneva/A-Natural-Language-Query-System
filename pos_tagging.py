# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'),
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    with open("sentences.txt", "r") as f:
        dict = {}
        words_list = set()
        for line in f:
            words = line.split(" ")
            for w in words:
                w_split = w.split("|")
                if (w_split[1] == "NN" ):
                    if (w_split[0] in dict):
                        if(dict[w_split[0]] == "NNS"):
                            words_list.add(w_split[0])
                    else:
                        dict.update({w_split[0]:"NN"})
                if (w_split[1] == "NNS"):
                    if (w_split[0] in dict):
                        if (dict[w_split[0]] == "NN"):
                            words_list.add(w_split[0])
                    else:
                        dict.update({w_split[0]:"NNS"})
        return  words_list

unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""
    # add code here
    stem = ""
    if (s in unchanging_plurals_list):
        stem = s
    if (re.match("[a-z]*men", s)):
        stem = s[:-3] + "man"
    if (re.match("[a-z]*[^sxyzaeiou]s", s) and not s.endswith("chs") and not s.endswith("shs")):
            stem = s[:-1]
    if (re.match("[a-z]*[aeiou]ys", s)):
            stem = s[:-1]
    if (re.match("[a-z][a-z]*[^aeiou]ies", s)):
            stem = s[:-3] + 'y'
    if (re.match("[^aeiou]ies", s)):
            stem = s[:-1]
    if (re.match("[a-z]*(oes|xes|ches|shes|sses|zzes)", s)):
            stem = s[:-2]
    if (re.match("[a-z]*[^s]ses", s)):
            stem = s[:-1]
    if (re.match("[a-z]*[^iosxz]es", s) and not s.endswith("ches") and not s.endswith("shes")):
            stem = s[:-1]
    return stem

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    # add code here
    tags = []
    for w in lx.getAll("P"):
        if (w == wd):
            tags.append("P")
    for w in lx.getAll("A"):
        if (w == wd):
            tags.append("A")
    for w in lx.getAll("N"):
        if (w == wd):
            if (w == noun_stem(w)):
                tags.append("Ns")
                tags.append("Np")
            else:
                if (noun_stem(w) == ""):
                    tags.append("Ns")
                else:
                    tags.append("Np")
        elif (w == noun_stem(wd)):
            tags.append("Np")
    for w in lx.getAll("I"):
        if (w == wd):
            if (verb_stem(w) == ""):
                tags.append("Ip")
            else:
                tags.append("Is")
        elif (w == verb_stem(wd)):
            tags.append("Is")
    for w in lx.getAll("T"):
        if (w == wd):
            if (verb_stem(w) == ""):
                tags.append("Tp")
            else:
                tags.append("Ts")
        elif (w == verb_stem(wd)):
            tags.append("Ts")
    if (wd in function_words):
        for (w, t) in function_words_tags:
            if (w == wd):
                tags.append(t)

    return tags


def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.
