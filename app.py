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


# get URLs list
def search_google(google_api, google_engine_id, query):
    service = build("customsearch", "v1", developerKey=google_api)
    res = service.cse().list(q=query, cx=google_engine_id, ).execute()
    URLs = []
    for item in res['items']:
        URLs.append(item['link'])
        #print item,"\n"
    return URLs


# get plain text of each url
def get_plain_text(url):
    response = urllib2.urlopen(url)
    html_doc = response.read() # get html doc
    soup = BeautifulSoup(html_doc,'html.parser')
    # kill all script and style elements
    for script in soup(["script", "style", "sup"]):
        script.decompose()  # rip it out

    # seperate text with span content
    for script in soup.find_all('span'):
        script.string = '. '+ script.get_text() + '.'

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
def get_sentences(plain_txt, relation_group):
    doc = client.annotate(text=plain_txt, properties=properties_pipeline1)
    sentences = []

    # print doc.tree_as_string()

    for sentence in doc.sentences:
        # print "for this sentence: it contains: "
        # print sentence.__str__()
        if is_filtered_by_entity_type(sentence, relation_group):
            continue
        newsentence = from_words_to_sentence(sentence)
        if len(newsentence) > 2000:
            continue
        # print "----" + newsentence
        # newsentence = newsentence.encode('utf8','replace')
        sentences.append(newsentence)
    # print 'sentences: ', sentences
    return sentences


# check valid relation
def is_valid_relation(type1, type2, relation_group):
    if relation_group == "_NR":
        return False
    type_set = type_dict[relation_group]
    valid_type1 = 'PEOPLE' if type_set[0] == 'PERSON' else type_set[0]
    if len(type_set) == 2:
        valid_type2 = 'PEOPLE' if type_set[1] == 'PERSON' else type_set[1]
    else:
        valid_type2 = valid_type1
    if type1 == valid_type1 and type2 == valid_type2:
        return True
    return False


# analyze sentences to extract tuples
def extract_tuples(query_sentences, relation_group, threshold):
    # return [] # test
    num_of_relations = 0  # the overall number of relations extracted from this website
    num_of_valid_relations = 0 # the number of valid relations (including relations whose confidence below threshold)
    tuples = []
    type_set = type_dict[relation_group]
    # valid_type1 = 'PEOPLE' if type_set[0] == 'PERSON' else type_set[0]
    # valid_type2 = 'PEOPLE' if type_set[1] == 'PERSON' else type_set[1]
    # print 'valid types: ', valid_type1, '--', valid_type2

    try:
        for sentence in query_sentences:
            # print " --- ", sentence
            doc = client.annotate(text=[sentence.encode('utf-8')], properties=properties_pipeline2)
            relations = doc.sentences[0].relations
            if len(relations) is 0:
                continue
            try:
                for relation in relations:
                    if not relation:
                        continue
                    probability_dic = sorted(relation.probabilities.items(), key=lambda (k, v) : -float(v))
                    # print "Relation:::::::", relation, "\ntype:::::", relation.probabilities.keys()[0]
                    if is_valid_relation(relation.entities[0].type, relation.entities[1].type, probability_dic[0][0]):
                        num_of_relations += 1  # count relations

                    if probability_dic[0][0] == relation_group:
                        word1 = relation.entities[0].value
                        type1 = relation.entities[0].type
                        word2 = relation.entities[1].value
                        type2 = relation.entities[1].type
                        # print "we get a tuple: ", word1, type1, word2, type2
                        confidence = float(relation.probabilities[relation_group])
                        # print "type::::", type1, "--", type2
                        if not is_valid_relation(type1, type2, relation_group):
                            # print "however we dont want it"
                            continue
                        num_of_valid_relations += 1  # count valid relations
                        print '=============== EXTRACTED RELATION ==============='
                        print 'Sentence:' , sentence.replace("-LRB-", "(").replace("-RRB-",")")
                        print 'Relation Type:', relation_group, ' | ' \
                              'Confidence=', confidence, ' | ' \
                              'EntityType1=', type1, ' | ' \
                              'EntityValue1=', word1, ' | ' \
                              'EntityType2=', type2, ' | ' \
                              'EntityValue2=', word2
                        print '============== END OF RELATION DESC =============='

                        # save tuples whose confidence above threshold
                        # print "confidence is : ", confidence
                        if confidence >= threshold:
                            tup = []
                            tup.append((word1, type1))
                            tup.append((word2, type2))
                            tup.append(round(confidence,3))
                            tuples.append(tup)
                            # print 'here is one tuple: the tuple looks like this:'
                            # print tup
            except:
                print '---------- Relation Error ----------'
                raise
        print 'Relations extracted from this website: ' , num_of_valid_relations , ' (Overall: ' , num_of_relations , ')'
        # print tuples
        return tuples
    except:
        print '-------- Sentence Error ----------'
        raise


# result_tuples is a dic
# key is (entity1 entity2)
# value is confidence
def relation_print_format(sorted_tuple_list, relation_type, k):
    num = k if len(sorted_tuple_list)>=k else len(sorted_tuple_list)
    print 'Pruning relations below threshold...\n' \
          'Number of tuples after pruning: ' , num , '\n' \
          '================== ALL RELATIONS ================='
    type_set = type_dict[relation_type]
    for tuple in sorted_tuple_list[0:num]:
        # key looks like : (Gates, PEOPEL, Microsoft, ORGANIZATION)
        # value is 0.379
        tuple_set = tuple[0].split(',')
        entity1 = str(tuple_set[0] +' ('+('PEOPLE' if tuple_set[1] == 'PERSON' else tuple_set[1])+')').ljust(37)
        entity2 = str(tuple_set[2] +' ('+('PEOPLE' if tuple_set[3] == 'PERSON' else tuple_set[3])+')')
        print "Relation Type: {}| Confidence: {}| Entity #1: {}|Entity #2: {}".format(relation_type.ljust(20), str(decimal.Decimal("%.3f" % float(tuple[1]))).ljust(10), entity1, entity2)


def main(api_key, engine_id, relation_id, threshold, query, k):

    relation_group = groups[relation_id-1]

    ##################################
    #    Print Format - Parameters
    ##################################
    print 'Parameters:\n' \
          'Client key      = ', api_key, '\n' \
          'Engine key      = ', engine_id, '\n' \
          'Relation        = ', relation_group, '\n' \
          'Threshold       = ', threshold, '\n' \
          'Query           = ', query, '\n' \
          '# of Tuples     = ', k
    ###################################
    #    End of Printing Parameters
    ###################################

    visited_tuples = set()
    visited_urls = set()
    visited_queries = set()
    tuple_dict = dict()
    round = 0
    while len(tuple_dict) < k:
        try:
            round = round + 1
            # Google CSE
            # print 'query: ', query
            print "fetching urls form Google CSE..."
            print "=========== Iteration: "+str(round)+" - Query: "+ query+" ==========="
            URLs = search_google(api_key, engine_id, query)
            # URLs = ['https://www.youtube.com/watch?v=rOqMawDj0LQ']
            visited_queries.add(query)
            for url in URLs:
                if url not in visited_urls:
                    print "Processing: ", url
                    visited_urls.add(url)
                    # a. retreive webpage b. extract plain text
                    try:
                        plain_text = get_plain_text(url)
                        sentences = get_sentences(plain_text, relation_group)
                        # print sentences
                        # analyze sentences to extract tuples
                        # print "extracting relations..."
                        tuples = extract_tuples(sentences, relation_group, threshold)
                        if not tuples:
                            continue
                        if len(tuples) > 0:
                            # remove dup
                            # tup -----  [('Gates', 'PEOPLE'), ('Microsoft', 'ORGANIZATION'), 0.379]
                            for t in tuples:
                                # hashing_key = t[0][0]+","+t[0][1]+";"+t[1][0]+","+t[1][1]
                                hashing_key = t[0][0]+","+t[0][1]+","+t[1][0]+","+t[1][1]
                                # word1 , type1, word2, type2
                                if hashing_key in visited_tuples:
                                    tuple_dict[hashing_key] = max(tuple_dict[hashing_key], float(t[2]))
                                    continue
                                visited_tuples.add(hashing_key)
                                tuple_dict[hashing_key] = float(t[2])
                    except:
                        print "timeout, continue to next url..."
            # sort to generate new query
            # print tuple_dict
            sorted_tuple_list = sorted(tuple_dict.items(), key=lambda (k, v): -v)
            # looks like [('Corporation Allen', 0.268), ('Allen Corporation', 0.26)]
            # print sorted_tuple_list

            relation_print_format(sorted_tuple_list,relation_group, k)

            found_a_new_query = False
            for tup in sorted_tuple_list:
                # potential_query = tup[0][0] + " " + tup[1][0]
                potential_query = tup[0]
                if potential_query not in visited_queries:
                    query = potential_query
                    found_a_new_query = True
                    # print "potential_query is :", potential_query
                    break
            if not found_a_new_query:
                print "Cannot find >=k results with q and k for t. Exit."
                sys.exit(0)

        except:
            print "---------While Loop Error-----------"
            raise
    print 'Program reached ' + str(k) + ' number of tuples. Shutting down...'
    sys.exit(0)


if __name__ == '__main__':
    api_key = GOOGLE_API
    engine_id = GOOGLE_ENGINE_ID
    r = 4 # Work_For
    t = 0.35
    q = "bill gates microsoft"
    k = 10

    if len(sys.argv) == 2 and sys.argv[1] == 'test':
        main(api_key, engine_id, r, t, q, k)
    if len(sys.argv) != 7:
         print "Usage: python app.py <google api key> <google engine id> <r> <t> <q> <k>\n", \
             "<google api key> is your Google Custom Search API Key\n", \
             "<google engine id> is your Google Custom Search Engine ID\n", \
             "<r> is an integer between 1 and 4, indicating the relation to extract\n", \
             "<t> is a real number between 0 and 1, indicating the \"extraction confidence threshold,\" " \
             "which is the minimum extraction confidence that we request for the tuples in the output\n" \
             "<q> is a \"seed query,\" which is a list of words in double quotes corresponding to " \
             "a plausible tuple for the relation to extract \n" \
             "<k> is an integer greater than 0, indicating the number of tuples that we request in the output\n"
         sys.exit()

    if len(sys.argv) == 7:
         api_key = sys.argv[1]
         engine_id = sys.argv[2]
         r = int(sys.argv[3])
         t = float(sys.argv[4])
         q = sys.argv[5]
         k = int(sys.argv[6])

    main(api_key, engine_id, r, t, q, k)
