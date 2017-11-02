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


Keys
--------
1. Google Custom Search API Key

         AIzaSyARFSgO3Kiuu3IOtEL8UwdIbrS7SiB43qo

2. Google Custom Search Engine ID

         018258045116810257593:z1fmkqqt_di

Internal Design
---------


1. About Stanford NLP

	We have two pipeline properties. The pipeline1’s annotators is “tokenize, ssplit, pos, lemma, ner”, which is used to separate sentence. And pipeline2’s annotators is “tokenize, ssplit, pos, lemma, ner, parse, relation”, which is used to extract relations.

2. Get plain text of one websit

	We use urllib2 package to get the html doc of a website. In order to get useful plain text, we rip content with tag “script”, “style” out. And since there will be lots of spans. We add “.” at the start and the end of each span text, avoiding several spans forming a sentences, which is not valid. After that, we concatenate every part of plain text as a whole string. And this string will be passed to Stanford NLP pipeline1.

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


