import re, sys
from googleapiclient.discovery import build
import urllib2
from bs4 import BeautifulSoup
from NLPCore import NLPCoreClient

# reload(sys)
# sys.setdefaultencoding('utf-8')

GOOGLE_API = "AIzaSyARFSgO3Kiuu3IOtEL8UwdIbrS7SiB43qo"
GOOGLE_ENGINE_ID = "018258045116810257593:z1fmkqqt_di"

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
        # print item
        # print "URL: ", item['link']
        # append url into url list
        URLs.append(item['link'])
        #print item,"\n"
    return URLs

# get plain text of each url
def get_plain_text(url):
    response = urllib2.urlopen(url)
    html_doc = response.read() # get html doc
    soup = BeautifulSoup(html_doc,'html.parser')
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.decompose()  # rip it out

    # get text
    text = soup.get_text()
    text = ''
    for string in soup.stripped_strings:
        text = text + ' ' + string
    # text = text.encode()
    print 'text: ', text
    # return as an array format
    return [text.encode('utf-8')]

# get sentences from plain text
def get_sentences(plain_txt):
    doc = client.annotate(text=plain_txt, properties=properties_pipeline1)
    sentences = []
    for sentence in doc.sentences:
        newsentence = ""
        for x in sentence.tokens:
            newsentence += " " + x.word
        # newsentence = newsentence.encode('utf8','replace')
        sentences.append(newsentence.encode('utf-8'))
    # print 'sentences: ', sentences
    return sentences

# analyze sentences to extract tuples
def extract_tuples(sentences, relation_group, threshold):
    tuples = []
    doc = client.annotate(text=sentences, properties=properties_pipeline2)
    for index in range(0, len(sentences)):
        # print index, " --- ", doc.sentences[index].relations
        if len(doc.sentences[index].relations) is 0:
            continue
        if not doc.sentences[index].relations[0]:
            print 'len 0'
            continue
        # if doc.sentences[index].relations[0].probabilities.keys()[0] is not relation_group:
        #     continue
        word1 = doc.sentences[0].entities[0].value
        word2 = doc.sentences[0].entities[1].value
        confidence = float(doc.sentences[index].relations[0].probabilities[relation_group])
        # print '/t', confidence
        # if the most confident group is relation_group
        if doc.sentences[index].relations[0].probabilities.key()[0] is relation_group:
            print '== == == == == == == = EXTRACTED RELATION == == == == == == == ='
            print 'Sentence: ' , doc.sentences[index]
            print 'Relation Type: ', relation_group,
            tuple = []
            tuple.append(word1)
            tuple.append(word2)
            tuple.append(confidence)
            tuples.append(tuple)
            # print tuple
    return tuples






if __name__ == '__main__':
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
    relation_id = sys.argv[3]  # relation to extract
                     # 1 is for Live_In, 2 is for Located_In, 3 is for OrgBased_In, and 4 is for Work_For
    if relation_id<1 or relation_id>4:
        print "<r> is an integer between 1 and 4, please input a valid value"
        sys.exit()
    threshold = sys.argv[4]  # extraction confidence threshold
    if threshold>1 or threshold<0:
        print '<t> is a real number between 0 and 1, indicating the \"extraction confidence threshold, '
        print 'please input a valid value'
        sys.exit()
    query = sys.argv[5]  # seed query
    number_of_tuples = sys.argv[6]  # the number of tuples that we request in the output


    # start iteration
    result_tuples = []

    for url in URLs:
        plain_text = get_plain_text(url)
        sentences = get_sentences(plain_text)
        tuples = extract_tuples(sentences, relation_group, threshold)
        if len(tuples) <1:
            continue
        else:
            result_tuples.extend(tuples)
    result_tuples = sorted(result_tuples, key=lambda x: -float(x[2]))


    '''

    #############################################
    #               Debug
    #############################################


    relation_id = 4
    query = "bill gates microsoft".encode('utf-8')
    threshold = 0.35


    relation_group = groups[relation_id-1]
    number_of_tuples = 10



        ##################################
        #    Print Format - Parameters
        ##################################
    print 'Parameters:\n' \
          'Client key        = ', GOOGLE_API, ''\
          '\nEngine key      = ', GOOGLE_ENGINE_ID, ''\
          '\nRelation        = ', relation_group, ''\
          '\nThreshold       = ', threshold, '' \
          '\nQuery           = ', query, ''\
          '\n# of Tuples     = ', number_of_tuples

        ###################################
        #    End of Printing Parameters
        ###################################

    # get 10 urls
    # URLs = search_google(GOOGLE_API, GOOGLE_ENGINE_ID, query)

    URLs = ['https://news.microsoft.com/exec/bill-gates/', 'https://en.wikipedia.org/wiki/Bill_Gates', 'https://www.theverge.com/2017/8/15/16148370/bill-gates-microsoft-shares-sale-2017', 'https://www.biography.com/people/bill-gates-9307520', 'http://www.telegraph.co.uk/technology/0/bill-gates/', 'https://www.cnbc.com/2017/09/25/bill-gates-microsoft-ceo-satya-nadella-talk-about-leadership.html', 'http://www.zdnet.com/article/bill-gates-stake-in-microsoft-is-now-just-1-3-percent/', 'https://www.wsj.com/articles/a-rare-joint-interview-with-microsoft-ceo-satya-nadella-and-bill-gates-1506358852', 'https://twitter.com/billgates', 'https://www.youtube.com/watch?v=rOqMawDj0LQ']


    print "URLs: ", URLs
    # test_URLs = []
    # test_URLs.append(URLs[0])
    result_tuples = []

    for url in URLs:
        plain_text = get_plain_text(url)
        sentences = get_sentences(plain_text)
        tuples = extract_tuples(sentences, relation_group, threshold)
        if len(tuples) <1:
            continue
        else:
            result_tuples.extend(tuples)
    result_tuples = sorted(result_tuples, key=lambda x: -float(x[2]))
    print "tuples:  " ,result_tuples
    for res in result_tuples:
        print res[0], '--', res[1], '--', res[2]

    #############################################
    #             End of Debug
    #############################################

