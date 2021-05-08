IMPORTANT: ne pas lancer le programme plusieurs fois de suite dans un espace de temps rapproché. L'accès à l'API Twitter est restreint par un certain nombre de tweets. Si on ne respecte pas ça, une exception de type "rate limit exceeded" s'affiche sur le terminal.


CRÉATION DE L'APPLICATION TWITTER:

1.Allez sur le site: https://twitter.com/?lang=fr
2.Si vous n'avez pas de compte, créez-en un; sinon, identifiez-vous et accédez aux paramètres de votre compte.
3.Une fois cela fait, cliquez sur l'onglet "applications" qui apparaît à gauche de l'écran.
4.Définissez les données de votre application Twitter: saisissez le nom,la description, l'URL de votre site pour l'application.
5.Générez vos clés en cliquant sur "Create my access token", en veillant à bien choisir le type d'accès à Twitter (lecture seulement, lecture et écriture...).
6.Récupérez les 4 clés: Consumer Key, Consumer Secret, OAuth Access Token, OAuth Access Token Secret.



EXÉCUTION DU PROGRAMME:

7.Allez au fichier "fonctionsAux.py" et remplissez les champs "Consumer Key, Consumer Secret, OAuth Access Token, OAuth Access Token Secret" (ligne 20 à 23) par les clés précédemment récupérées.
8.Pensez à installer le "package installer" de Python "pip" si vous ne l'avez pas déjà, en tapant la commande: 
					pip install -U pip
9.Installez les packets: -numpy
						 -nltk
						 -tweepy
						 -contractions
						 -unidecode
						 -flask

	Avec la commande: pip install <package> 

10.Exécutez le programme "ProgrammePrincipal.py".
11.Copiez l'URL qui va s'afficher sur votre terminal dans la barre de recherche de votre navigateur. Une page "Detection of Twitter opinions" devrait s'afficher.

12.Une fois le domaine saisi et après un moment, les dictionnaires d'adjectifs positifs/négatifs ainsi que quelques exemples de tweets devraient s'afficher. Si vous préférez voir des dictionnaires/tweets sur des domaines déjà traités, cliquez sur l'un des liens en bas de la page d'accueil.


P.S: si vous voulez varier le nombre de tweets à recupérer, il faut modifier la variable "maxTweets" qui se trouve dans le fichier "programmePrincipal.py" ligne 60. Dans ce cas, il faudra aussi modifier la variable "tw_block_size" (ligne 61) qui représente le nombre de tweets par requête (et donc par mot).