# DetectionOpinionsTwitter

Projet réalisé dans le cadre du travail d'étude et de recherche (TER) de L3.

## Description

 * Dans le cadre de ce projet, nous avons développé un système permettant la détection d'opinions exprimées dans les tweets. Nous avons pour cela développé une méthode récursive permettant la construction de deux dictionnaires d'adjectifs : un dictionnaire positif et un dictionnaire négatif. Ces dictionnaires nous ont permis de classer les tweets selon leurs opinions sans utiliser des techniques de machine learning ou de deep learning.
 
 * Nous avons donc :
 	* Récupérer les tweets pour un domaine donné à partir de Twitter.
 	* Nettoyer les tweets et extrait les adjectifs pertinents.
 	* Remplis deux dictionnaires d'adjectifs positifs et négatifs.
 	* Nettoyé les dictionnaires au fur et à mesure en appliquant un système de poids sur les adjectifs.
 	
 * Arrêt du programme lorsque plus aucun adjectif pertinent est ajouté aux dictionnaires au bout d'un certain nombre de boucle.
 
 * Nous avons ensuite utilisé les dictionnaires construits pour la détection d'opinions sur de nouveaux tweets pour un domaine donné `Ex: Brexit`. 
 
* Une interface a été développée à la fin afin de saisir le domaine et d'afficher les résultats du système.

## Schéma général :

![alt text](https://github.com/NihedB/DetectionOpinionsTwitter/blob/main/schema_twitter.png?raw=true)


## Prérequis 


Le programme s'exécute avec Python 3. Les dépendances de packages attendues sont répertoriées dans le fichier `requirements.txt` pour PIP. Pour les obtenir,  veuillez exécuter la commande :


```
pip install -r requirements.txt
```

## Outils

* [Tweepy](https://www.tweepy.org/) : Accès à l'API Twitter et récupération des tweets.
* [NLTK](https://www.nltk.org/) : Traitement des tweets.
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) : Développement de l'interface web.



## Auteurs

* Nihed Bendahman
* Maroua Dorsaf Djelouat
* Cheimae Assarar
