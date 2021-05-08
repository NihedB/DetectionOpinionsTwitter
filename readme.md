----------------------------------------------------------------------------------------------------

LIBRAIRIE :
(note : vous devez toujours ouvrir le terminal dans lib pour effectuer ces actions)
(note2 : chaque librairie installer ne sera pas pusher sur le git. Par conséquent, tous le monde doit installer les librairies nécessaire sur leur machine)


Pour installer NTLTK :
	- pip install nltk -t .
	- pip install numpy -t .

	- Maintenant on peut installer tous le package de NLTK (long et lourd), ou juste ce qui est nécessaire.
	Pour tout installer :
		- python -m nltk.downloader -d ../nltk_data all
	Pour installer ce qui est nécessaire :
		- python -m nltk.downloader -d ../nltk_data punkt
		- python -m nltk.downloader -d ../nltk_data averaged_perceptron_tagger
		- python -m nltk.downloader -d ../nltk_data maxent_ne_chunker
		- python -m nltk.downloader -d ../nltk_data words
		- python -m nltk.downloader -d ../nltk_data treebank

Pour installer une librairie, faire la commande suivante :
	- pip install NOM_LIBRAIRIE -t .

----------------------------------------------------------------------------------------------------

(note : il faut ouvrir le terminal dans le dossier lib)

Pour utiliser le POS-tagger, Tockenizer et Parser de Stanford, il faut suivre les stapes suivantes:

	1. Télécharger les packages nécessaires de CoreNLP en utilisant le lien suivant :
		wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-02-27.zip

	2. Décompressez les packages téléchargés :
		unzip stanford-corenlp-full-2018-02-27.zip

	3. accédez au dossier des packages telechargés:
		cd stanford-corenlp-full-2018-02-27

	4. Lancez la commande suivante dans le terminal:
		java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
		-preload tokenize,ssplit,pos,lemma,ner,parse,depparse \
		-status_port 9000 -port 9000 -timeout 15000 & 

	5. Une fois fini, importez les bibliotheques dans votre notebook :
		from nltk.parse import CoreNLPParser
		from nltk.parse.corenlp import CoreNLPDependencyParser

	5. Une fois fini, utilisez ce code source pour faire des requêtes au Server de Stanford :
		# Lexical Parser
		parser = CoreNLPParser(url='http://localhost:9000')

		# Parse tokenized text.
		list(parser.parse('What is the airspeed of an unladen swallow ?'.split()))

		# Parse raw string.
		list(parser.raw_parse('What is the airspeed of an unladen swallow ?'))

		# Neural Dependency Parser
		dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
		parses = dep_parser.parse('What is the airspeed of an unladen swallow ?'.split())


		# Tokenizer
		parser = CoreNLPParser(url='http://localhost:9000')
		list(parser.tokenize('What is the airspeed of an unladen swallow?'))


		# POS Tagger
		pos_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='pos')
		list(pos_tagger.tag('What is the airspeed of an unladen swallow ?'.split()))

		# NER Tagger
		ner_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
		list(ner_tagger.tag(('Rami Eid is studying at Stony Brook University in NY'.split())))
