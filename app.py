import re, sys
from googleapiclient.discovery import build
import urllib2
from bs4 import BeautifulSoup
from NLPCore import NLPCoreClient

STANFORD_PATH = '../stanford-corenlp-full-2017-06-09'
client = NLPCoreClient(STANFORD_PATH)
properties_pipeline1 = {
	"annotators": "tokenize,ssplit,pos,lemma,ner",
	"parse.model": "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz",
	"ner.useSUTime": "0"
	}
properties_pipeline2 = {
	"annotators": "tokenize,ssplit,pos,lemma,ner,parse,relation",
	"parse.model": "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz",
	"ner.useSUTime": "0"
	}
groups = ['Live_In', 'Located_In', 'OrgBased_In', 'Work_For']

# get URLs list
def search_google(google_api, google_engine_id, query):
    service = build("customsearch", "v1", developerKey=google_api)
    res = service.cse().list(q=query, cx=google_engine_id, ).execute()
    URLs = []
    for item in res['items']:
        print item
        print "URL: ", item['link']
        # append url into url list
        URLs.append(item['link'])
        #print item,"\n"
    print URLs

# get plain text of each url
def get_plain_text(url):
    response = urllib2.urlopen(url)
    html_doc = response.read() # get html doc
    soup = BeautifulSoup(html_doc, "html.parser")
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.decompose()  # rip it out

    # get text
    text = soup.get_text()
    text = ''
    for string in soup.stripped_strings:
        text = text + ' ' + string
    print text
    return text

# get sentences from plain text
def get_sentences(plain_txt):
    doc = client.annotate(text=plain_txt, properties=properties_pipeline1)
    sentences = []
    for sentence in doc.sentences:
        newsentence = ""
        for x in sentence.tokens:
            newsentence += " " + x.word
        sentences.append(newsentence)
    print sentences
    return sentences

# analyze sentences to extract tuples
def extract_tuples(sentences, group_id, threshold):
    tuples = []
    group = groups[group_id]
    doc = client.annotate(text=sentences, properties=properties_pipeline2)
    for index in range(0, len(sentences)):
        if len(doc.sentences[index].relations) is 0\
                or doc.sentences[1].relations[0].probabilities.keys()[0] is not group:
            continue
        word1 = doc.sentences[0].entities[0].value
        word2 = doc.sentences[0].entities[1].value
        confidence = doc.sentences[0].relations[0].probabilities[group]
        if confidence>=threshold:
            tuple = []
            tuple.append(word1)
            tuple.append(word2)
            tuple.append(confidence)
            tuples.append(tuple)
    return tuples






if __name__ == '__main__':

    api = "AIzaSyARFSgO3Kiuu3IOtEL8UwdIbrS7SiB43qo"
    engine = "018258045116810257593:z1fmkqqt_di"
    query = "per se"
    # search_google(api, engine, query)
    # get_plain_text('http://www.baidu.com')
    # plain_txt = "Bill Gates works at Microsoft. Sergei works at Google. abc is abc, and it is not def"
    # get_sentence(plain_txt)
    test = ['1','2']
    test.append('3')

    # sort
    # sort(tuples, key=lambda x: -x[3])



    '''
    if len(sys.argv) >=0 and len(sys.argv)<7:
        print "Usage: python Main.py <google api key> <google engine id> <r> <t> <q> <k>\n", \
            "<google api key> is your Google Custom Search API Key\n", \
            "<google engine id> is your Google Custom Search Engine ID\n", \
            "<r> is an integer between 1 and 4, indicating the relation to extract\n", \
            "<t> is a real number between 0 and 1, indicating the \"extraction confidence threshold,\" " \
            "which is the minimum extraction confidence that we request for the tuples in the output\n"\
            "<q> is a \"seed query,\" which is a list of words in double quotes corresponding to " \
            "a plausible tuple for the relation to extract \n"\
            "<k> is an integer greater than 0, indicating the number of tuples that we request in the output\n"
        sys.exit()

    google_api = sys.argv[1]
    google_engine_id = sys.argv[2]
    r = sys.argv[3]  # relation to extract
                     # 1 is for Live_In, 2 is for Located_In, 3 is for OrgBased_In, and 4 is for Work_For
    t = sys.argv[4]  # extraction confidence threshold
    q = sys.argv[5]  # seed query
    k = sys.argv[6]  # the number of tuples that we request in the output
    '''
