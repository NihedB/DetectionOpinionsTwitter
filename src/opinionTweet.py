#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import numpy as np
import nltk
import re
import json
from nltk import word_tokenize
import tweepy
import os
import re
import unicodedata
from unidecode import unidecode
import fonctionsAux

#fonction qui calcule la somme des poids des adjectifs présents dans un tweet et retourne 0 si l'opinion est neutre, 1 si elle est positive, -1 si négative.
def opinionTweet(opinion, positif, negatif, notAdjs, advAdjs):
    somme=0
    tempo=nltk.pos_tag(word_tokenize(opinion))
    i=0
    while i<len(tempo):
        if(tempo[i][1]=="JJ"):
            adj=tempo[i][0].lower()
            if(adj in positif):
                if(adj in notAdjs):
                    somme-=1
                elif(adj in advAdjs):
                	somme+=3
                else:
                    somme+=2
            elif(adj in negatif):
                if(adj in notAdjs):
                    somme+=1
                elif(adj in advAdjs):
                	somme-=3
                else:
                    somme-=2
        i+=1
    if somme==0:
        return 0
    elif somme >0:
        return 1
    else:
        return -1