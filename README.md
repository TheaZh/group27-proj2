# COMS6111 Project 2
COMS6111 Project 2

Group Name
--------
Project 2 Group 27

Group Member
--------
   Qianwen Zheng (qz2271)

   Jiajun Zhang (jz2793)

Files
--------

  	group27-proj2
	├── NLPCore.py
	├── README.md
	├── app.py
	├── data.py
	├── props.properties
	├── requirements.txt
	└── transcript.txt


Run
--------

1. Install Java 8 and download Stanford CoreNLP software suite

	Install Java 8 (the default JDK is Java 7 under ubuntu 14.04, so we installed Java 8 in other ways)

		# Run under Ubuntu 14.04 LTS
		sudo apt-get update
		sudo add-apt-repository ppa:webupd8team/java
		# make sure you do this
		sudo apt-get update
		# remeber to choose to agree the license
		sudo apt-get install oracle-java8-installer

	Get Stanford CoreNLP

		wget http://nlp.stanford.edu/software/stanford-corenlp-full-2017-06-09.zip
		sudo apt-get install unzip
		unzip stanford-corenlp-full-2017-06-09.zip        


2. Clone project   

	Install git if you haven't

		sudo apt-get install git

	then, clone project

		git clone https://github.com/TheaZh/group27-proj2.git


3. Navigate to folder

		cd group27_proj2

4. Install dependencies

		sudo apt install python-pip
		sudo pip install -r requirements.txt

5. Run program

		python app.py <google api key> <google engine id> <r> <t> <q> <k>

   \<google api key> -- your Google Custom Search API Key

   \<google engine id> -- your Google Custom Search Engine ID

   \<r> -- an integer between 1 and 4, indicating the relation to extract

   \<t> -- the extraction confidence threshold

   \<q> -- seed query

   \<k> -- the number of tuples that we request in the output



Internal Design
---------


1. About Stanford NLP

	We have two pipeline properties. The pipeline1’s annotators is “tokenize, ssplit, pos, lemma, ner”, which is used to separate sentence. And pipeline2’s annotators is “tokenize, ssplit, pos, lemma, ner, parse, relation”, which is used to extract relations.

2. Get plain text of one websit

	We use urllib2 package to get the html doc of a website. In order to get useful plain text, we rip content with tag “script”, “style” out. And since there will be lots of spans. We add “.” at the start and the end of each span text, avoiding several spans forming a sentences, which is not valid. After that, we concatenate every part of plain text as a whole string. And this string will be passed to Stanford NLP pipeline1. If the program have a time out when we retrieve this website, it will skip this website and move on.

3. Process Sentences

	Since there will be a lot of sentences, most of which are invalid (Here an invalid sentence means it definitely doesn’t include the relation we are looking for. For example, if we are looking for a “Live_In” relation, then we will abort sentences which don’t contains both “PERSON” and “LOCATION” entities.), we just want to pass valid sentences to next pipeline. So we create a dictionary, where the key is relation type and the value is entity types it contains. For each sentence, we get a set to store its entity types. Then, we check if it contains all entity types of the relation we are looking for. If it doesn’t, we will not append this sentence to our sentences list.

4. Tuples extraction

	Given the sentence list, we pass the sentence one by one to pipeline2. For each sentence, if relations can be extracted, we can get the relation type with the highest confidence. If the relation is not valid (Here a valid relation means the two entities’ types match the required entity types. For example, if it is a “Work_For” relation, then two entity types have to be “PEOPLE” and “ORGANIZATION”.), we will skip this relation. If the relation type matches the one that we’re looking for and the entity types match types of this relation, we print this relation. And if the relation’s confidence is above the threshold, we store it in our list of result tuples, with the format of ((word1, type1), (word2, type2), confidence).

5. Deduplicate

	We create a dictionary to store tuples with confidence above threshold. The key is “word1, type1, word2, type2” and the value is tuple’s confidence. During the progress, there will be tuples with same entities but different confidence. If one tuple shows again with higher confidence, we will update the confidence of this tuple in the dictionary, keeping that the value in dictionary always be the highest confidence of this tuple. This dictionary will be printed as result. So it guarantees there is no duplicated tuples.

6. While loop

	The whole algorithm is in a while loop. In each round, the dictionary we talked above will be sorted according to it value (i.e. tuple confidence). And we have a set contains used query. If in this round, the result dictionary contains more than k tuples, we print the top-k tuples sorted in decreasing order by extraction confidence, and then stop the program. If there are less than k tuples, we select one tuple with highest confidence that has not yet been used for querying in result dictionary. And create a new tuple with both entity values together, and start a new round.

Step 3
--------
Use a set to contain all the visited URLs. Privide the unvisited url to Google CSE.

* Get content of the webpage according to the url within a try clause in case of timeout.      
* Extract plain text from the html document using BeautifulSoup. The original html doc is much likely to contain many texts that are useless. For example, there are texts in <stype> tag, which is useless and may influence our result. Therefore, we filter this useless texts to get more accurate result.
* Use Stanford CoreNLP for entity detecting and relation extraction:       
__Pipeline1__ (entity detecting): use pipeline1 to extract sentences from the plaintext. In each sentence, ff there are entities that follows the relation group (e.g. relation group is Work_For, we only need the sentence which contains entity type of both PEOPLE and ORGANIZATION), add this sentence to our sentences list. Otherwise, we skip this sentence.     
__Pipeline2__ (relation extraction): use pipeline2 to extract relations from the sentences passed from pipeline1. For a relation of one sentence, sort its probabilities.item() in descending order by confidence score. Then, we can get the most confident relation type is the first item. If this relation type is same with the one we are looking for, the tuple is considered a new candidate. After obtaining a new candidate, firstly decide if the entity types are related to the relation group and filter the invalid ones. Then check the confidence score, if confidence score is greater than or equal to threshold, update the tuple confidence if we have already obtained this relation tuple before, select the higher confidence value and update the dictionary. If it is not in the dictionary, add it.


Keys
--------
1. Google Custom Search API Key

         AIzaSyARFSgO3Kiuu3IOtEL8UwdIbrS7SiB43qo

2. Google Custom Search Engine ID

         018258045116810257593:z1fmkqqt_di
