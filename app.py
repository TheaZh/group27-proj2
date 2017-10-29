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

# get a whole sentence
def from_words_to_sentence(sentence):
    newsentence = ""
    for x in sentence.tokens:
        newsentence += " " + x.word
    return newsentence
# get sentences from plain text
def get_sentences(plain_txt):
    doc = client.annotate(text=plain_txt, properties=properties_pipeline1)
    sentences = []
    for sentence in doc.sentences:
        newsentence = from_words_to_sentence(sentence)
        # newsentence = newsentence.encode('utf8','replace')
        sentences.append(newsentence.encode('utf-8'))
    # print 'sentences: ', sentences
    return sentences

# analyze sentences to extract tuples
def extract_tuples(query_sentences, relation_group, threshold):
    num_of_relations = 0  # the overall number of relations extracted from this website
    num_of_valid_relations = 0 # the number of valid relations (including relations whose confidence below threshold)
    tuples = []
    doc = client.annotate(text=query_sentences, properties=properties_pipeline2)
    sentences = doc.sentences
    for sentence in sentences:
        print " --- ", from_words_to_sentence(sentence)
        relations = sentence.relations
        if len(relations) is 0:
            continue
        for relation in relations:
            if not relation:
                # print 'len 0'
                continue
            num_of_relations += 1 # count relations
            # print "Relation:::::::", relation, "\ntype:::::", relation.probabilities.keys()[0]
            probability_dic = sorted(relation.probabilities.items(), key=lambda (k, v) : -float(v))
            if probability_dic[0][0] == relation_group:
                num_of_valid_relations += 1 # count valid relations
                word1 = relation.entities[0].value
                type1 = relation.entities[0].type
                word2 = relation.entities[1].value
                type2 = relation.entities[1].type
                confidence = float(relation.probabilities[relation_group])

                plain_sentence = from_words_to_sentence(sentence)

                print '============== EXTRACTED RELATION =============='
                print 'Sentence:' , plain_sentence
                print 'Relation Type:', relation_group, ' | ' \
                      'Confidence=', confidence, ' | ' \
                      'EntityType1=', type1, ' | ' \
                      'EntityValue1=', word1, ' | ' \
                      'EntityType2=', type2, ' | ' \
                      'EntityValue2=', word2
                print '============== END OF RELATION DESC =============='

                # save tuples whose confidence above threshold
                if confidence >= threshold:
                    tuple = []
                    tuple.append(word1+' ('+type1+')')
                    tuple.append(word2+' ('+type2+')')
                    tuple.append(round(confidence,3))
                    tuples.append(tuple)
            # print tuple
    print 'Relations extracted from this website: ' , num_of_valid_relations , ' (Overall: ' , num_of_relations , ')'
    return tuples


def relation_print_format(result_tuples, relation_type):
    print 'Pruning relations below threshold...\n' \
          'Number of tuples after pruning: ' , len(result_tuples) , '\n' \
          '================== ALL RELATIONS ================='
    for tuple in result_tuples:
        print "Relation Type: {}| Confidence: {}| Entity #1: {}|Entity #2: {}".format(relation_type.ljust(20),str(tuple[2]).ljust(10), tuple[0].ljust(37), tuple[1])






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
    threshold = 0.22


    relation_group = groups[relation_id-1]
    number_of_tuples = 10



        ##################################
        #    Print Format - Parameters
        ##################################
    print 'Parameters:\n' \
          'Client key      = ', GOOGLE_API, '\n'\
          'Engine key      = ', GOOGLE_ENGINE_ID, '\n'\
          'Relation        = ', relation_group, '\n'\
          'Threshold       = ', threshold, '\n' \
          'Query           = ', query, '\n'\
          '# of Tuples     = ', number_of_tuples

        ###################################
        #    End of Printing Parameters
        ###################################

    # get 10 urls
    # URLs = search_google(GOOGLE_API, GOOGLE_ENGINE_ID, query)

    URLs = ['https://en.wikipedia.org/wiki/Bill_Gates']
            # 'https://news.microsoft.com/exec/bill-gates/',
            #'https://www.theverge.com/2017/8/15/16148370/bill-gates-microsoft-shares-sale-2017', 'https://www.biography.com/people/bill-gates-9307520', 'http://www.telegraph.co.uk/technology/0/bill-gates/', 'https://www.cnbc.com/2017/09/25/bill-gates-microsoft-ceo-satya-nadella-talk-about-leadership.html', 'http://www.zdnet.com/article/bill-gates-stake-in-microsoft-is-now-just-1-3-percent/', 'https://www.wsj.com/articles/a-rare-joint-interview-with-microsoft-ceo-satya-nadella-and-bill-gates-1506358852', 'https://twitter.com/billgates', 'https://www.youtube.com/watch?v=rOqMawDj0LQ']


    print "URLs: ", URLs
    # test_URLs = []
    # test_URLs.append(URLs[0])
    result_tuples = []

    for url in URLs:
        print 'Processing: ' + url
        # plain_text = get_plain_text(url)
        plain_text = ['William Henry Gates III (born October 28, 1955) is an American business magnate , investor , author , philanthropist , and co-founder of the Microsoft Corporation along with Paul Allen.']
        sentences = get_sentences(plain_text)
        print sentences
        tuples = extract_tuples(sentences, relation_group, threshold)
        if len(tuples) <1:
            continue
        else:
            result_tuples.extend(tuples)

    # sorted by confidence (descending)
    result_tuples = sorted(result_tuples, key=lambda x: -float(x[2]))

    relation_print_format(result_tuples, relation_group)
    # print "tuples:  " ,result_tuples
    # for res in result_tuples:
    #     print res[0], '--', res[1], '--', res[2]

    #############################################
    #             End of Debug
    #############################################

