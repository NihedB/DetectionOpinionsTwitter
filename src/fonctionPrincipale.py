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

tweets=[]

seuilColonne=4
seuilLigne=7

#Fonction recursive qui récupère les tweets, les stocke dans un fichier, et appelle à tour de rôle les fonctions remplissage et filtre. 
#cette fonction s'arrête quand il n'y a plus de nouvelles colonnes rajoutées dans dicoPositif (resp. dicoNégatif). 
def fonctionPrincipale(dico, mots, tweets,p, fin,new, tweetCount,nbOcc, notAdjs, interdit, domaine, advAdjs, maxTweets, tw_block_size):
	if (p==fin):
		return 
	else:
		tweets=[] 
		c=fonctionsAux.recuperationTweets(new, tweetCount, notAdjs, domaine, advAdjs, maxTweets, tw_block_size)
		fichier=open("tweets.json", "r")
		for ligne in fichier.readlines():
			array = ligne
			data = json.loads(array)
			tweets.append(data)
		fichier.close()
		fonctionsAux.remplissage(tweets,dico, notAdjs, advAdjs)
		k=len(dico)
		new=fonctionsAux.filtre(dico,mots,nbOcc,interdit, domaine)
		fin=len(dico)    
		fonctionPrincipale(dico, mots, tweets, k, fin, new, c, nbOcc, notAdjs, interdit, domaine, advAdjs, maxTweets, tw_block_size)


