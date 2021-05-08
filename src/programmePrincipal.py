#!/usr/bin/env python2
#  coding: utf-8 
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
from flask import Flask, request, render_template, url_for, redirect
import fonctionPrincipale
import fonctionsAux
import opinionTweet
import contractions
from random import *



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

iniNeg=['bad','wrong', 'horrible', 'sad', 'terrible', 'boring', 'awful']


tweets=[]
domaine=""  

maxTweets = 2000 # Nombre de tweets max a récupérer par domaine
tw_block_size = 100 # Nombre de tweets par requête (et donc par mot)
app = Flask(__name__)

#---------------------------------------partie interface---------------------------------------
a=open( "donnees.json", 'w')
a.write("")
a.close()

@app.route('/', methods=['GET','POST'])
def Research():
    global domaine
    if request.method == 'POST':
        domaine = '{domaine}'.format(domaine=request.form['domaine'])
        return redirect('result')
    return render_template('home.html')



opinion={}
@app.route("/result")
def result():

	fonctionPrincipale.fonctionPrincipale(dicoPositif, positif, tweets, 0, -1, positif, 0, nbOccPositif, notAdjs,negatif, domaine, advAdjs, maxTweets, tw_block_size)
	fonctionPrincipale.fonctionPrincipale(dicoNegatif, negatif, tweets, 0, -1, negatif, 0, nbOccNegatif, notAdjs,positifBis, domaine, advAdjs, maxTweets, tw_block_size)
	fonctionsAux.supBruits(nbOccPositif, positif)


	fonctionsAux.supBruits(nbOccNegatif, negatif)

	fonctionsAux.compareAdj(positif, negatif, nbOccPositif, nbOccNegatif)
	
	fonctionsAux.mise_a_jour(advAdjs, positif, negatif)
	fonctionsAux.mise_a_jour(notAdjs, positif, negatif)

	
	compteur=0
	i=0
	j=0
	fich=open("donnees.json","r")
	lignes=fich.readlines()
	while(i<20):
		j=randint(1, len(lignes))
		data = json.loads(lignes[j])
		data=fonctionsAux.nettoyage(data)
		data=fonctionsAux.deEmojify(data)
		data=contractions.fix(data)
		a=opinionTweet.opinionTweet(data, positif, negatif, notAdjs, advAdjs)
		opinion[compteur]=[]
		opinion[compteur].append(data)
		opinion[compteur].append(a)
		compteur+=1
		i+=1
	
	fich.close()
	return render_template('result1.html', positif=positif, negatif=negatif, opinion=opinion, positifBis=positifBis, iniNeg=iniNeg)


@app.route("/netflix")
def netflix():
	pos=[]
	neg=[]
	op={}
	cpt=0
	fich=open("netflixPos.txt", "r")
	lignes=fich.readlines()
	for ligne in lignes:
		ligne=ligne.replace('\n',"")
		pos.append(ligne)
	fich.close()

	fich=open("netflixNeg.txt", "r")
	lignes=fich.readlines()
	for ligne in lignes:
		ligne=ligne.replace('\n',"")
		neg.append(ligne)
	fich.close()

	fich=open("Netflixopinions.json", "r")
	lignes=fich.readlines()
	for ligne in lignes:
		data = json.loads(ligne)
		data=fonctionsAux.nettoyage(data)
		data=fonctionsAux.deEmojify(data)
		data=contractions.fix(data)
		a=opinionTweet.opinionTweet(data, pos, neg, notAdjs, advAdjs)
		op[cpt]=[]
		op[cpt].append(data)
		op[cpt].append(a)
		cpt+=1
	fich.close()
	return render_template("netflix.html", pos=pos, neg=neg, op=op, positifBis=positifBis, iniNeg=iniNeg)


@app.route("/cars")
def cars():
	pos=[]
	neg=[]
	op={}
	cpt=0
	fich=open("carsPos.txt", "r")
	lignes=fich.readlines()
	for ligne in lignes:
		ligne=ligne.replace('\n',"")
		pos.append(ligne)
	fich.close()

	fich=open("carsNeg.txt", "r")
	lignes=fich.readlines()
	for ligne in lignes:
		ligne=ligne.replace('\n',"")
		neg.append(ligne)
	fich.close()

	fich=open("carsOp.json", "r")
	lignes=fich.readlines()
	for ligne in lignes:
		data = json.loads(ligne)
		data=fonctionsAux.nettoyage(data)
		data=fonctionsAux.deEmojify(data)
		data=contractions.fix(data)
		a=opinionTweet.opinionTweet(data, pos, neg, notAdjs, advAdjs)
		op[cpt]=[]
		op[cpt].append(data)
		op[cpt].append(a)
		cpt+=1
	fich.close()
	return render_template("cars.html", pos=pos, neg=neg, op=op, positifBis=positifBis, iniNeg=iniNeg)



if __name__ == '__main__':
    app.run()



