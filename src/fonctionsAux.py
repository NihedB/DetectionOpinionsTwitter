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
import contractions





#les 4 clés pour l'authentification à l'application twitter
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""



language="en" #spécification de la langue (on récupère des tweets écrits en anglais)

tweets=[] #initialisation du tableau tweet (un tableau stockant les tweets lus à partir du fichier tweets.json)

seuilColonne=4 #Un adjectif doit apparaître dans 4 colonnes min. 
seuilLigne=7  #Un adjectif doit apparaître au moins 7 fois. 


#initialisation du tableau positif avec des adjectifs "généraux" (adjectifs avec lesquels on fait les premières requêtes)
positif=['good','nice', 'great', 'wonderful', 'best','amazing','funny' ,'awesome','favorite','cool']

#copie du tableau positif dont on aura besoin pour interdire les adjectifs positifs lors du lancement des requêtes sur les adjectifs
#négatifs (on ne pouvait utiliser "positif" car il sera modifié au fur et à mesure).
positifBis=['good','nice', 'great', 'wonderful', 'best','amazing','funny' ,'awesome','favorite','cool']

#initialisation du tableau négatif avec des adjectifs "généraux" (adjectifs avec lesquels on fait les premières requêtes)
negatif=['bad','wrong', 'horrible', 'sad', 'terrible', 'boring', 'awful']

#dictionnaires dans lequel on stocke les adjectifs contenus dans positif (resp negatif) comme des clés. les valeurs de ces clés sont des tableaux,
#dans lesquels on stocke les adjectifs qui sont apparus avec la clés et leur nombre d'apparitions.
dicoPositif={'good':[],'nice':[], 'great':[], 'wonderful':[],'best':[],'amazing':[],'funny':[],'awesome':[], 'favorite': [],'cool':[]}
dicoNegatif={ 'bad':[],'wrong':[], 'horrible':[], 'sad':[], 'terrible':[], 'boring':[], 'awful':[]}

#dictionnaires dans lequel on stocke le nombre d'occurrences final des adjectifs
nbOccPositif={'good':0, 'nice':0, 'great':0, 'wonderful':0,'best':0,'amazing':0,'funny':0,'awesome':0,'favorite':0,'cool':0}
nbOccNegatif={'bad':0, 'wrong':0, 'horrible':0, 'sad':0, 'terrible':0, 'boring':0, 'awful':0}


#tableau pour stocker des mots considérés comme étant des adjectifs par l'analyseur morphosyntaxique (nltk.pos_tag), et qui apparaissent
#beaucoup dans les tweets,pour pouvoir les interdire dans nos requêtes.
motsInterdits=['other','only','such', 'much','own', 'next','so']
#tableau pour stocker des adjectifs précédés par une négation (ex: not good, neither good...)
notAdjs=[]
#tableau pour stocker des adjectifs précédés par un adverbe (ex: so good, realy good...)
advAdjs=[]
#tableau contenant des mots qui définissent la négation
negation=['not','neither','nor','no']
#tableau contenant des adverbes
adverbes=['very', 'so','too','really']



#connexion à l'application twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api=tweepy.API(auth)



class Adj(object):
    def __init__(self, adj, nb):
        self.adj = adj
        self.nb = nb
    def get_adj (self):
        return self.adj
    def get_nb (self):
        return self.nb

    def set_nb(self, v):
    	self.nb=v



#fonction qui incremente le nombre d'occurrence du mot "fragment" dans la colonne cle de dico (dicoPositif/ dicoNegatif) si ce fragment existe deja
def check_adj (dico, cle, fragment, nb):
	i=0
	while i<len(dico[cle]):
		if(dico[cle][i].get_adj()==fragment):
			nb=dico[cle][i].get_nb()+1
			dico[cle][i].set_nb(nb)
		i+=1
	return nb

#fonction qui enlève les url, identifiants utilisateurs et caractères spéciaux des tweets (met des espaces entre quelques caractères)
def nettoyage(tweet):
	replace_chars = [
        [r'[\w\.-]+@[\w\.-]+', "", True],
        [r'([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)'," ",True],
        [r'\d+'," ",True],
        ["\"", "", False],
        [r'(\/+)'," ",True],
        ["@","",False],
        ["#","",False],
        ["_"," ", False],
        [".", " . ", False],
        [",", " , ", False],
        [";", " ; ", False],
        ["?", " ? ", False],
        [":", " : ", False],
        ["!", " ! ", False],
        [" '", " ", False],
        ["' ", " ", False]
    
    ]

	for e in replace_chars:
		if (e[2]):
			tweet = re.sub(e[0], e[1], tweet, flags=re.MULTILINE)
		else:
			tweet = tweet.replace(e[0], e[1])

	return tweet

#fonction qui enlève les émojis des tweets
def deEmojify(inputString):
	returnString = ""
	for character in inputString:
		try:
			character.encode("ascii")
			returnString += character
		except UnicodeEncodeError:
			returnString += ''
	return returnString


##fonction qui supprime de positif (resp négatif) les adjectifs, si leur nombre d'occurrences est inférieur au seuil (ces adjectis ont 
#été crées lors du dernier appel, donc le filtre n'est pas appliqué sur eux)
def supBruits(nbOcc, mots):
    for i in nbOcc:
        if nbOcc[i]<seuilLigne:
            mots.remove(i)

#fonction qui compare le nombre d'occurrences d'un adjectif qui apparait à la fois dans positif et négatif. Si la différence est<15, elle le supprime.
def compareAdj(positif, negatif, nbOccPositif, nbOccNegatif):
    for i in nbOccPositif:
        for j in nbOccNegatif:
            if i==j:
                difference=abs(nbOccPositif[i]-nbOccNegatif[j])
                if difference<=15:
                    positif.remove(i)
                    negatif.remove(j)
                else:
                    if(nbOccPositif[i]>nbOccNegatif[j]):
                        negatif.remove(j)
                    else:
                        positif.remove(i)


#fonction qui met à jour les tableaux "advAdjs" et "notAdjs".
def mise_a_jour(tab, positif, negatif):
    i=0
    while(i<len(tab)):
        if tab[i] not in positif and tab[i] not in negatif:
            tab.remove(tab[i])
            i-=1
        i+=1



#fonction qui traite les tweets récupérés et rempli dicoPositif, dicoNegatif, advAdjs et notAdjs avec les nouveaux adjectifs trouvés.
def remplissage(tweet, dico, notAdjs, advAdjs):
    t=0

    while t<len(tweet):
        chaine=tweet[t]
        chaine=nettoyage(chaine)
        chaine=deEmojify(chaine)
        chaine=contractions.fix(chaine)
        print(chaine)
        tempo=nltk.pos_tag(word_tokenize(chaine))
        k=0
        bufAdj=[]
        while k<len(tempo):
            if(tempo[k][1]=="JJ"):
                bufAdj.append(tempo[k][0])
                k+=1
            elif(not(k==len(tempo)-1) and tempo[k][0] in negation and tempo[k+1][1]=='JJ'):
                notAdj=tempo[k][0]+" "+tempo[k+1][0]
                bufAdj.append(notAdj)
                if notAdj not in notAdjs:
                    notAdjs.append(notAdj)
                k+=2
            elif(not(k==len(tempo)-1) and tempo[k][0] in adverbes and tempo[k+1][1]=='JJ'):
                advAdj=tempo[k][0]+" "+tempo[k+1][0]
                bufAdj.append(advAdj)
                if advAdj not in advAdjs:
                    advAdjs.append(advAdj)
                k+=2
            elif(not(k==len(tempo)-1) and not(k+1==len(tempo)-1) and tempo[k][0] in negation and tempo[k+1][0] in adverbes and tempo[k+2][1]=='JJ'):
                notAdj=tempo[k][0]+" "+tempo[k+1][0]+" "+tempo[k+2][0]
                bufAdj.append(notAdj)
                if notAdj not in notAdjs:
                    notAdjs.append(notAdj)
                k+=3
            else:
                k+=1
        j=0
        while j<len(bufAdj):
            cle=bufAdj[j]
            if(dico.has_key(cle)):
                i=0
                while i<len(bufAdj):
                    if(bufAdj[i]==cle):
                        i+=1
                    else:
                        nb=1
                        nb=check_adj(dico, cle, bufAdj[i], nb)

                        if nb==1:
                            objet=Adj(bufAdj[i].lower(),nb)
                            dico[cle].append(objet)
                        i+=1

            j+=1
        t+=1


# fonction qui rajoute à "positif" et "negatif" les nouveaux adj vérifiant toutes les conditions de fitrage.
def filtre(dico, mots, nbOcc,interdit, domaine):
    k=0
    newWords=[]
    while k<len(dico):
        cle=mots[k]
        j=0
        while j<len(dico[cle]):
            if(dico[cle][j].get_adj().lower() in mots):
            	ad=dico[cle][j].get_adj().lower()
            	nbOcc[ad]+=dico[cle][j].get_nb()
                del dico[cle][j]
                j-=1
            else:
                apparait=1
                somme=dico[cle][j].get_nb()
                for c in dico:
                    i=0
                    trouve=False
                    while i<len(dico[c]) and not(trouve) and c!=cle :
                        if(dico[c][i].get_adj() == dico[cle][j].get_adj()):
                            somme+=(dico[c][i].get_nb())
                            apparait+=1
                            trouve=True
                        i+=1
                mot=dico[cle][j].get_adj()        
                if(apparait>=seuilColonne and somme>=seuilLigne and  mot not in domaine and mot not in motsInterdits and len(mot)>2 and mot not in interdit):
                    adj=mot.lower()
                    dico[adj]=[]
                    mots.append(adj)
                    nbOcc[adj]=somme
                    newWords.append(adj)
                    del dico[cle][j]
                    j-=1
             
            j+=1
        k+=1
    return newWords



def recuperationTweets(tab, tweetCount, notAdjs, domaine, advAdjs, maxTweets,tw_block_size):
    max_id = -1L
  
    i=0
    a=open( "tweets.json", 'w')
    nvF=open("donnees.json", "a")
    while i<len(tab) and tweetCount < maxTweets:
        if(tab[i] not in domaine and tab[i] not in motsInterdits and len(tab[i])>2 and tab[i] not in notAdjs and tab[i] not in advAdjs):
            query=domaine + " " + tab[i] +" -RT "
            print(query)
            try:
                if (max_id <= 0):
                    results = api.search(q=query, count=tw_block_size,lang=language, tweet_mode='extended')
                else:                    
                    results = api.search(q=query, count=tw_block_size, max_id=str(max_id - 1), lang=language, tweet_mode='extended')
                if not results:
                    i+=1
                    continue    
                for tweet in results:
                    with open( "tweets.json", 'a') as f:
                        f.write(json.dumps(tweet._json['full_text']))
                        nvF.write(json.dumps(tweet._json['full_text']))
                        f.write('\n') 
                        nvF.write('\n') 
                tweetCount += len(results)                     
                max_id = results[-1].id
                i+=1 
            except tweepy.TweepError as e:
                print("Une erreur est intervenue. Pour poursuivre le processus de collecte, relancer la commande")
                print("")
                print("Error : " + str(e))
                return
        else:
            i+=1
    a.close()
    nvF.close()
    return tweetCount  
