import re, sys
from googleapiclient.discovery import build
import urllib2
from bs4 import BeautifulSoup

# get URLs list
def search_google(google_api, google_engine_id, query):
    service = build("customsearch", "v1", developerKey=google_api)
    res = service.cse().list(q=query, cx=google_engine_id, ).execute()
    URLs = []
    for item in res['items']:
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
    text = ''
    for string in soup.stripped_strings:
        text = text + ' ' + string
    return text


if __name__ == '__main__':

    api = "AIzaSyARFSgO3Kiuu3IOtEL8UwdIbrS7SiB43qo"
    engine = "018258045116810257593:z1fmkqqt_di"
    query = "baidu"
    #search_google(api, engine, query)
    get_plain_text('http://www.baidu.com')




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
