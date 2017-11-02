import os, sys
from googleapiclient.discovery import build
import urllib2
from bs4 import BeautifulSoup
from NLPCore import NLPCoreClient
import decimal

# reload(sys)
# sys.setdefaultencoding('utf-8')

GOOGLE_API = "AIzaSyARFSgO3Kiuu3IOtEL8UwdIbrS7SiB43qo"
GOOGLE_ENGINE_ID = "018258045116810257593:z1fmkqqt_di"

STANFORD_PATH = '../stanford-corenlp-full-2017-06-09'
# STANFORD_PATH = os.path.abspath("stanford-corenlp-full-2017-06-09")
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

type_dict = dict()
type_dict['Live_In'] = ['PERSON', 'LOCATION']
type_dict['Located_In'] = ['LOCATION']
type_dict['OrgBased_In'] = ['ORGANIZATION', 'LOCATION']
type_dict['Work_For'] = ['ORGANIZATION','PERSON']
# get plain text of each url
def get_plain_text(url):
    response = urllib2.urlopen(url)
    # html_doc = response.read() # get html doc
    html_doc = '''
    <p> a is b, c is d</p>
    <span> abcdef</span>
    '''
    soup = BeautifulSoup(html_doc,'html.parser')
    # kill all script and style elements
    for script in soup(["script", "style", "sup"]):
        script.decompose()  # rip it out

    for s in soup.find_all('span'):
        s.string = '. '+ s.get_text() + '.'
    text = ''
    for string in soup.stripped_strings:
    # for string in soup.find_all('p'):
        text = text + ' ' + string
    return [text.encode('utf-8')]


# get a whole sentence
def from_words_to_sentence(sentence):
    newsentence = ""
    for x in sentence.tokens:
        newsentence += " " + x.word
    return newsentence


def is_filtered_by_entity_type(sentence, relation_group):
    entity_type_set = set()
    for token in sentence.tokens:
        entity_type_set.add(str(token.ner))
    for entity_type in type_dict[relation_group]:
        if entity_type not in entity_type_set:
            return True
    return False


# get sentences from plain text
def get_sentences(plain_txt):
    doc = client.annotate(text=plain_txt, properties=properties_pipeline1)
    sentences = []

    # print doc.tree_as_string()

    for sentence in doc.sentences:
        # print "for this sentence: it contains: "
        # print sentence.__str__()
        newsentence = from_words_to_sentence(sentence)
        if len(newsentence) > 2000:
            continue
        print "----" + newsentence
        # newsentence = newsentence.encode('utf8','replace')
        sentences.append(newsentence)
    # print 'sentences: ', sentences
    return sentences



print '--------------------------------'
print '--------------------------------'

url = 'https://news.microsoft.com/exec/bill-gates/'
text = get_plain_text(url)
sentences = get_sentences(text)

# str = "Bill Gates - News Center Skip to Main Content Learn more Office Windows Surface Xbox Deals Support More Software Windows apps OneDrive Outlook Skype OneNote PCs & Devices PCs & tablets Accessories VR & mixed reality Microsoft HoloLens Entertainment Xbox games PC games Windows digital games Movies & TV Business Microsoft Azure Microsoft Dynamics 365 Microsoft 365 Cloud platform Enterprise Data platform Developer & IT Microsoft ."
# doc = client.annotate(text=[str], properties=properties_pipeline1)
# print doc.tree_as_string()