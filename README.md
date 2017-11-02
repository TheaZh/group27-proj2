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


Keys
--------
1. Google Custom Search API Key

         AIzaSyARFSgO3Kiuu3IOtEL8UwdIbrS7SiB43qo

2. Google Custom Search Engine ID

         018258045116810257593:z1fmkqqt_di

Internal Design
---------


Step 3
--------


