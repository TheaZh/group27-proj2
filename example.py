from NLPCore import NLPCoreClient

text = ["Bill Gates works at Microsoft. Sergei works at Google. abc is abc, and it is not def"]

#path to corenlp
STANFORD_PATH = '../stanford-corenlp-full-2017-06-09'
client = NLPCoreClient(STANFORD_PATH)
properties = {
	"annotators": "tokenize,ssplit,pos,lemma,ner",
	"parse.model": "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz",
	"ner.useSUTime": "0"
	}
doc = client.annotate(text=text, properties=properties)
# print(doc.sentences[0].relations[0])
# print '--------------------------------'
# print '--------------------------------'
# print(doc.tree_as_string())
newsentence = ""
for x in doc.sentences[0].tokens:
	newsentence += " " + x.word
print(newsentence)