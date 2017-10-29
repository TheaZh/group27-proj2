from NLPCore import NLPCoreClient

text = ["Bill Gates ."]

#path to corenlp
STANFORD_PATH = '../stanford-corenlp-full-2017-06-09'
client = NLPCoreClient(STANFORD_PATH)
properties = {
	"annotators": "tokenize,ssplit,pos,lemma,ner,parse,relation",
	"parse.model": "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz",
	"ner.useSUTime": "0"
	}
doc = client.annotate(text=text, properties=properties)
# print doc.sentences[0].entities[0].type, ': ', doc.sentences[0].entities[0].value
# print doc.sentences[0].entities[1].type, ': ', doc.sentences[0].entities[1].value
print doc.sentences[0].relations
if len(doc.sentences[0].relations) is 0:
	print 'none'

# print '======='
# print doc.sentences[1].entities[0].type, ': ', doc.sentences[1].entities[0].value
# print doc.sentences[1].entities[1].type, ': ', doc.sentences[1].entities[1].value
# print doc.sentences[1].relations[0]
# print doc.sentences[1].relations[0].probabilities.keys()[0]


print '--------------------------------'
print '--------------------------------'
# confidence_dic = doc.sentences[0].relations[0].probabilities
# for key in confidence_dic.iterkeys():
# 	print key
# 	print confidence_dic[key]

# print '--------------------------------'
# print '--------------------------------'
# print(doc.tree_as_string())
# newsentence = ""
# for x in doc.sentences[0].tokens:
# 	newsentence += " " + x.word
# print(newsentence)

'''
Relation with id: RelationMention-1, made up of the following entities: [Entity with ID: EntityMention-1, value: Gates, and type: PEOPLE. Entity with ID: EntityMention-2, value: Microsoft, and type: ORGANIZATION. ], and the following probabilities:[{'OrgBased_In': '0.39717886837934685', '_NR': '0.18107178574908858', 'Live_In': '0.1005973115454124', 'Located_In': '0.11392489275533632', 'Work_For': '0.2072271415708158'}].
<?xml version="1.0" ?><sentences>
      	<sentence id="1">
        		<tokens>
          			<token id="1">
            				<word>Bill</word>
            				<lemma>Bill</lemma>
            				<CharacterOffsetBegin>0</CharacterOffsetBegin>
            				<CharacterOffsetEnd>4</CharacterOffsetEnd>
            				<POS>NNP</POS>
            				<NER>PERSON</NER>
          			</token>
          			<token id="2">
            				<word>Gates</word>
            				<lemma>Gates</lemma>
            				<CharacterOffsetBegin>5</CharacterOffsetBegin>
            				<CharacterOffsetEnd>10</CharacterOffsetEnd>
            				<POS>NNP</POS>
            				<NER>PERSON</NER>
          			</token>
          			<token id="3">
            				<word>works</word>
            				<lemma>work</lemma>
            				<CharacterOffsetBegin>11</CharacterOffsetBegin>
            				<CharacterOffsetEnd>16</CharacterOffsetEnd>
            				<POS>VBZ</POS>
            				<NER>O</NER>
          			</token>
          			<token id="4">
            				<word>at</word>
            				<lemma>at</lemma>
            				<CharacterOffsetBegin>17</CharacterOffsetBegin>
            				<CharacterOffsetEnd>19</CharacterOffsetEnd>
            				<POS>IN</POS>
            				<NER>O</NER>
          			</token>
          			<token id="5">
            				<word>Microsoft</word>
            				<lemma>Microsoft</lemma>
            				<CharacterOffsetBegin>20</CharacterOffsetBegin>
            				<CharacterOffsetEnd>29</CharacterOffsetEnd>
            				<POS>NNP</POS>
            				<NER>ORGANIZATION</NER>
          			</token>
          			<token id="6">
            				<word>.</word>
            				<lemma>.</lemma>
            				<CharacterOffsetBegin>29</CharacterOffsetBegin>
            				<CharacterOffsetEnd>30</CharacterOffsetEnd>
            				<POS>.</POS>
            				<NER>O</NER>
          			</token>
        		</tokens>
        		<parse>(ROOT (S (NP (NNP Bill) (NNP Gates)) (VP (VBZ works) (PP (IN at) (NP (NNP Microsoft)))) (. .))) </parse>
        		<dependencies type="basic-dependencies">
          			<dep type="root">
            				<governor idx="0">ROOT</governor>
            				<dependent idx="3">works</dependent>
          			</dep>
          			<dep type="compound">
            				<governor idx="2">Gates</governor>
            				<dependent idx="1">Bill</dependent>
          			</dep>
          			<dep type="nsubj">
            				<governor idx="3">works</governor>
            				<dependent idx="2">Gates</dependent>
          			</dep>
          			<dep type="case">
            				<governor idx="5">Microsoft</governor>
            				<dependent idx="4">at</dependent>
          			</dep>
          			<dep type="nmod">
            				<governor idx="3">works</governor>
            				<dependent idx="5">Microsoft</dependent>
          			</dep>
          			<dep type="punct">
            				<governor idx="3">works</governor>
            				<dependent idx="6">.</dependent>
          			</dep>
        		</dependencies>
        		<dependencies type="collapsed-dependencies">
          			<dep type="root">
            				<governor idx="0">ROOT</governor>
            				<dependent idx="3">works</dependent>
          			</dep>
          			<dep type="compound">
            				<governor idx="2">Gates</governor>
            				<dependent idx="1">Bill</dependent>
          			</dep>
          			<dep type="nsubj">
            				<governor idx="3">works</governor>
            				<dependent idx="2">Gates</dependent>
          			</dep>
          			<dep type="case">
            				<governor idx="5">Microsoft</governor>
            				<dependent idx="4">at</dependent>
          			</dep>
          			<dep type="nmod:at">
            				<governor idx="3">works</governor>
            				<dependent idx="5">Microsoft</dependent>
          			</dep>
          			<dep type="punct">
            				<governor idx="3">works</governor>
            				<dependent idx="6">.</dependent>
          			</dep>
        		</dependencies>
        		<dependencies type="collapsed-ccprocessed-dependencies">
          			<dep type="root">
            				<governor idx="0">ROOT</governor>
            				<dependent idx="3">works</dependent>
          			</dep>
          			<dep type="compound">
            				<governor idx="2">Gates</governor>
            				<dependent idx="1">Bill</dependent>
          			</dep>
          			<dep type="nsubj">
            				<governor idx="3">works</governor>
            				<dependent idx="2">Gates</dependent>
          			</dep>
          			<dep type="case">
            				<governor idx="5">Microsoft</governor>
            				<dependent idx="4">at</dependent>
          			</dep>
          			<dep type="nmod:at">
            				<governor idx="3">works</governor>
            				<dependent idx="5">Microsoft</dependent>
          			</dep>
          			<dep type="punct">
            				<governor idx="3">works</governor>
            				<dependent idx="6">.</dependent>
          			</dep>
        		</dependencies>
        		<dependencies type="enhanced-dependencies">
          			<dep type="root">
            				<governor idx="0">ROOT</governor>
            				<dependent idx="3">works</dependent>
          			</dep>
          			<dep type="compound">
            				<governor idx="2">Gates</governor>
            				<dependent idx="1">Bill</dependent>
          			</dep>
          			<dep type="nsubj">
            				<governor idx="3">works</governor>
            				<dependent idx="2">Gates</dependent>
          			</dep>
          			<dep type="case">
            				<governor idx="5">Microsoft</governor>
            				<dependent idx="4">at</dependent>
          			</dep>
          			<dep type="nmod:at">
            				<governor idx="3">works</governor>
            				<dependent idx="5">Microsoft</dependent>
          			</dep>
          			<dep type="punct">
            				<governor idx="3">works</governor>
            				<dependent idx="6">.</dependent>
          			</dep>
        		</dependencies>
        		<dependencies type="enhanced-plus-plus-dependencies">
          			<dep type="root">
            				<governor idx="0">ROOT</governor>
            				<dependent idx="3">works</dependent>
          			</dep>
          			<dep type="compound">
            				<governor idx="2">Gates</governor>
            				<dependent idx="1">Bill</dependent>
          			</dep>
          			<dep type="nsubj">
            				<governor idx="3">works</governor>
            				<dependent idx="2">Gates</dependent>
          			</dep>
          			<dep type="case">
            				<governor idx="5">Microsoft</governor>
            				<dependent idx="4">at</dependent>
          			</dep>
          			<dep type="nmod:at">
            				<governor idx="3">works</governor>
            				<dependent idx="5">Microsoft</dependent>
          			</dep>
          			<dep type="punct">
            				<governor idx="3">works</governor>
            				<dependent idx="6">.</dependent>
          			</dep>
        		</dependencies>
        		<MachineReading>
          			<entities>
            				<entity id="EntityMention-1">					PEOPLE
              					<span end="2" start="1"/>
              					<probabilities/>
            				</entity>
            				<entity id="EntityMention-2">					ORGANIZATION
              					<span end="5" start="4"/>
              					<probabilities/>
            				</entity>
          			</entities>
          			<relations>
            				<relation id="RelationMention-1">					OrgBased_In
              					<arguments>
                						<entity id="EntityMention-1">							PEOPLE
                  							<span end="2" start="1"/>
                  							<probabilities/>
                						</entity>
                						<entity id="EntityMention-2">							ORGANIZATION
                  							<span end="5" start="4"/>
                  							<probabilities/>
                						</entity>
              					</arguments>
              					<probabilities>
                						<probability>
                  							<label>OrgBased_In</label>
                  							<value>0.39717886837934685</value>
                						</probability>
                						<probability>
                  							<label>Work_For</label>
                  							<value>0.2072271415708158</value>
                						</probability>
                						<probability>
                  							<label>_NR</label>
                  							<value>0.18107178574908858</value>
                						</probability>
                						<probability>
                  							<label>Located_In</label>
                  							<value>0.11392489275533632</value>
                						</probability>
                						<probability>
                  							<label>Live_In</label>
                  							<value>0.1005973115454124</value>
                						</probability>
              					</probabilities>
            				</relation>
            				<relation id="RelationMention-2">					Work_For
              					<arguments>
                						<entity id="EntityMention-2">							ORGANIZATION
                  							<span end="5" start="4"/>
                  							<probabilities/>
                						</entity>
                						<entity id="EntityMention-1">							PEOPLE
                  							<span end="2" start="1"/>
                  							<probabilities/>
                						</entity>
              					</arguments>
              					<probabilities>
                						<probability>
                  							<label>Work_For</label>
                  							<value>0.2625665274406702</value>
                						</probability>
                						<probability>
                  							<label>OrgBased_In</label>
                  							<value>0.2589269913408607</value>
                						</probability>
                						<probability>
                  							<label>Located_In</label>
                  							<value>0.23011518386734892</value>
                						</probability>
                						<probability>
                  							<label>Live_In</label>
                  							<value>0.1381332361516736</value>
                						</probability>
                						<probability>
                  							<label>_NR</label>
                  							<value>0.11025806119944687</value>
                						</probability>
              					</probabilities>
            				</relation>
          			</relations>
        		</MachineReading>
      	</sentence>
      	<sentence id="2">
        		<tokens>
          			<token id="1">
            				<word>Sergei</word>
            				<lemma>Sergei</lemma>
            				<CharacterOffsetBegin>31</CharacterOffsetBegin>
            				<CharacterOffsetEnd>37</CharacterOffsetEnd>
            				<POS>NNP</POS>
            				<NER>PERSON</NER>
          			</token>
          			<token id="2">
            				<word>works</word>
            				<lemma>work</lemma>
            				<CharacterOffsetBegin>38</CharacterOffsetBegin>
            				<CharacterOffsetEnd>43</CharacterOffsetEnd>
            				<POS>VBZ</POS>
            				<NER>O</NER>
          			</token>
          			<token id="3">
            				<word>at</word>
            				<lemma>at</lemma>
            				<CharacterOffsetBegin>44</CharacterOffsetBegin>
            				<CharacterOffsetEnd>46</CharacterOffsetEnd>
            				<POS>IN</POS>
            				<NER>O</NER>
          			</token>
          			<token id="4">
            				<word>Google</word>
            				<lemma>Google</lemma>
            				<CharacterOffsetBegin>47</CharacterOffsetBegin>
            				<CharacterOffsetEnd>53</CharacterOffsetEnd>
            				<POS>NNP</POS>
            				<NER>ORGANIZATION</NER>
          			</token>
          			<token id="5">
            				<word>.</word>
            				<lemma>.</lemma>
            				<CharacterOffsetBegin>53</CharacterOffsetBegin>
            				<CharacterOffsetEnd>54</CharacterOffsetEnd>
            				<POS>.</POS>
            				<NER>O</NER>
          			</token>
        		</tokens>
        		<parse>(ROOT (S (NP (NNP Sergei)) (VP (VBZ works) (PP (IN at) (NP (NNP Google)))) (. .))) </parse>
        		<dependencies type="basic-dependencies">
          			<dep type="root">
            				<governor idx="0">ROOT</governor>
            				<dependent idx="2">works</dependent>
          			</dep>
          			<dep type="nsubj">
            				<governor idx="2">works</governor>
            				<dependent idx="1">Sergei</dependent>
          			</dep>
          			<dep type="case">
            				<governor idx="4">Google</governor>
            				<dependent idx="3">at</dependent>
          			</dep>
          			<dep type="nmod">
            				<governor idx="2">works</governor>
            				<dependent idx="4">Google</dependent>
          			</dep>
          			<dep type="punct">
            				<governor idx="2">works</governor>
            				<dependent idx="5">.</dependent>
          			</dep>
        		</dependencies>
        		<dependencies type="collapsed-dependencies">
          			<dep type="root">
            				<governor idx="0">ROOT</governor>
            				<dependent idx="2">works</dependent>
          			</dep>
          			<dep type="nsubj">
            				<governor idx="2">works</governor>
            				<dependent idx="1">Sergei</dependent>
          			</dep>
          			<dep type="case">
            				<governor idx="4">Google</governor>
            				<dependent idx="3">at</dependent>
          			</dep>
          			<dep type="nmod:at">
            				<governor idx="2">works</governor>
            				<dependent idx="4">Google</dependent>
          			</dep>
          			<dep type="punct">
            				<governor idx="2">works</governor>
            				<dependent idx="5">.</dependent>
          			</dep>
        		</dependencies>
        		<dependencies type="collapsed-ccprocessed-dependencies">
          			<dep type="root">
            				<governor idx="0">ROOT</governor>
            				<dependent idx="2">works</dependent>
          			</dep>
          			<dep type="nsubj">
            				<governor idx="2">works</governor>
            				<dependent idx="1">Sergei</dependent>
          			</dep>
          			<dep type="case">
            				<governor idx="4">Google</governor>
            				<dependent idx="3">at</dependent>
          			</dep>
          			<dep type="nmod:at">
            				<governor idx="2">works</governor>
            				<dependent idx="4">Google</dependent>
          			</dep>
          			<dep type="punct">
            				<governor idx="2">works</governor>
            				<dependent idx="5">.</dependent>
          			</dep>
        		</dependencies>
        		<dependencies type="enhanced-dependencies">
          			<dep type="root">
            				<governor idx="0">ROOT</governor>
            				<dependent idx="2">works</dependent>
          			</dep>
          			<dep type="nsubj">
            				<governor idx="2">works</governor>
            				<dependent idx="1">Sergei</dependent>
          			</dep>
          			<dep type="case">
            				<governor idx="4">Google</governor>
            				<dependent idx="3">at</dependent>
          			</dep>
          			<dep type="nmod:at">
            				<governor idx="2">works</governor>
            				<dependent idx="4">Google</dependent>
          			</dep>
          			<dep type="punct">
            				<governor idx="2">works</governor>
            				<dependent idx="5">.</dependent>
          			</dep>
        		</dependencies>
        		<dependencies type="enhanced-plus-plus-dependencies">
          			<dep type="root">
            				<governor idx="0">ROOT</governor>
            				<dependent idx="2">works</dependent>
          			</dep>
          			<dep type="nsubj">
            				<governor idx="2">works</governor>
            				<dependent idx="1">Sergei</dependent>
          			</dep>
          			<dep type="case">
            				<governor idx="4">Google</governor>
            				<dependent idx="3">at</dependent>
          			</dep>
          			<dep type="nmod:at">
            				<governor idx="2">works</governor>
            				<dependent idx="4">Google</dependent>
          			</dep>
          			<dep type="punct">
            				<governor idx="2">works</governor>
            				<dependent idx="5">.</dependent>
          			</dep>
        		</dependencies>
        		<MachineReading>
          			<entities>
            				<entity id="EntityMention-3">					PEOPLE
              					<span end="1" start="0"/>
              					<probabilities/>
            				</entity>
            				<entity id="EntityMention-4">					ORGANIZATION
              					<span end="4" start="3"/>
              					<probabilities/>
            				</entity>
          			</entities>
          			<relations>
            				<relation id="RelationMention-3">					OrgBased_In
              					<arguments>
                						<entity id="EntityMention-3">							PEOPLE
                  							<span end="1" start="0"/>
                  							<probabilities/>
                						</entity>
                						<entity id="EntityMention-4">							ORGANIZATION
                  							<span end="4" start="3"/>
                  							<probabilities/>
                						</entity>
              					</arguments>
              					<probabilities>
                						<probability>
                  							<label>OrgBased_In</label>
                  							<value>0.3986560745294246</value>
                						</probability>
                						<probability>
                  							<label>Work_For</label>
                  							<value>0.21265547493337847</value>
                						</probability>
                						<probability>
                  							<label>_NR</label>
                  							<value>0.1700988800618771</value>
                						</probability>
                						<probability>
                  							<label>Located_In</label>
                  							<value>0.11436850830249173</value>
                						</probability>
                						<probability>
                  							<label>Live_In</label>
                  							<value>0.10422106217282812</value>
                						</probability>
              					</probabilities>
            				</relation>
            				<relation id="RelationMention-4">					Work_For
              					<arguments>
                						<entity id="EntityMention-4">							ORGANIZATION
                  							<span end="4" start="3"/>
                  							<probabilities/>
                						</entity>
                						<entity id="EntityMention-3">							PEOPLE
                  							<span end="1" start="0"/>
                  							<probabilities/>
                						</entity>
              					</arguments>
              					<probabilities>
                						<probability>
                  							<label>Work_For</label>
                  							<value>0.262829962815225</value>
                						</probability>
                						<probability>
                  							<label>OrgBased_In</label>
                  							<value>0.25913697766720306</value>
                						</probability>
                						<probability>
                  							<label>Located_In</label>
                  							<value>0.23022532164522627</value>
                						</probability>
                						<probability>
                  							<label>Live_In</label>
                  							<value>0.13850668095733132</value>
                						</probability>
                						<probability>
                  							<label>_NR</label>
                  							<value>0.1093010569150142</value>
                						</probability>
              					</probabilities>
            				</relation>
          			</relations>
        		</MachineReading>
      	</sentence>
      	<sentence id="3">
        		<tokens>
          			<token id="1">
            				<word>abc</word>
            				<lemma>abc</lemma>
            				<CharacterOffsetBegin>56</CharacterOffsetBegin>
            				<CharacterOffsetEnd>59</CharacterOffsetEnd>
            				<POS>NN</POS>
            				<NER>O</NER>
          			</token>
          			<token id="2">
            				<word>is</word>
            				<lemma>be</lemma>
            				<CharacterOffsetBegin>60</CharacterOffsetBegin>
            				<CharacterOffsetEnd>62</CharacterOffsetEnd>
            				<POS>VBZ</POS>
            				<NER>O</NER>
          			</token>
          			<token id="3">
            				<word>abc</word>
            				<lemma>abc</lemma>
            				<CharacterOffsetBegin>63</CharacterOffsetBegin>
            				<CharacterOffsetEnd>66</CharacterOffsetEnd>
            				<POS>NN</POS>
            				<NER>O</NER>
          			</token>
          			<token id="4">
            				<word>,</word>
            				<lemma>,</lemma>
            				<CharacterOffsetBegin>66</CharacterOffsetBegin>
            				<CharacterOffsetEnd>67</CharacterOffsetEnd>
            				<POS>,</POS>
            				<NER>O</NER>
          			</token>
          			<token id="5">
            				<word>and</word>
            				<lemma>and</lemma>
            				<CharacterOffsetBegin>68</CharacterOffsetBegin>
            				<CharacterOffsetEnd>71</CharacterOffsetEnd>
            				<POS>CC</POS>
            				<NER>O</NER>
          			</token>
          			<token id="6">
            				<word>it</word>
            				<lemma>it</lemma>
            				<CharacterOffsetBegin>72</CharacterOffsetBegin>
            				<CharacterOffsetEnd>74</CharacterOffsetEnd>
            				<POS>PRP</POS>
            				<NER>O</NER>
          			</token>
          			<token id="7">
            				<word>is</word>
            				<lemma>be</lemma>
            				<CharacterOffsetBegin>75</CharacterOffsetBegin>
            				<CharacterOffsetEnd>77</CharacterOffsetEnd>
            				<POS>VBZ</POS>
            				<NER>O</NER>
          			</token>
          			<token id="8">
            				<word>not</word>
            				<lemma>not</lemma>
            				<CharacterOffsetBegin>78</CharacterOffsetBegin>
            				<CharacterOffsetEnd>81</CharacterOffsetEnd>
            				<POS>RB</POS>
            				<NER>O</NER>
          			</token>
          			<token id="9">
            				<word>def</word>
            				<lemma>def</lemma>
            				<CharacterOffsetBegin>82</CharacterOffsetBegin>
            				<CharacterOffsetEnd>85</CharacterOffsetEnd>
            				<POS>NN</POS>
            				<NER>O</NER>
          			</token>
        		</tokens>
        		<parse>(ROOT (S (S (NP (NN abc)) (VP (VBZ is) (NP (NN abc)))) (, ,) (CC and) (S (NP (PRP it)) (VP (VBZ is) (RB not) (NP (NN def)))))) </parse>
        		<dependencies type="basic-dependencies">
          			<dep type="root">
            				<governor idx="0">ROOT</governor>
            				<dependent idx="3">abc</dependent>
          			</dep>
          			<dep type="nsubj">
            				<governor idx="3">abc</governor>
            				<dependent idx="1">abc</dependent>
          			</dep>
          			<dep type="cop">
            				<governor idx="3">abc</governor>
            				<dependent idx="2">is</dependent>
          			</dep>
          			<dep type="punct">
            				<governor idx="3">abc</governor>
            				<dependent idx="4">,</dependent>
          			</dep>
          			<dep type="cc">
            				<governor idx="3">abc</governor>
            				<dependent idx="5">and</dependent>
          			</dep>
          			<dep type="nsubj">
            				<governor idx="9">def</governor>
            				<dependent idx="6">it</dependent>
          			</dep>
          			<dep type="cop">
            				<governor idx="9">def</governor>
            				<dependent idx="7">is</dependent>
          			</dep>
          			<dep type="neg">
            				<governor idx="9">def</governor>
            				<dependent idx="8">not</dependent>
          			</dep>
          			<dep type="conj">
            				<governor idx="3">abc</governor>
            				<dependent idx="9">def</dependent>
          			</dep>
        		</dependencies>
        		<dependencies type="collapsed-dependencies">
          			<dep type="root">
            				<governor idx="0">ROOT</governor>
            				<dependent idx="3">abc</dependent>
          			</dep>
          			<dep type="nsubj">
            				<governor idx="3">abc</governor>
            				<dependent idx="1">abc</dependent>
          			</dep>
          			<dep type="cop">
            				<governor idx="3">abc</governor>
            				<dependent idx="2">is</dependent>
          			</dep>
          			<dep type="punct">
            				<governor idx="3">abc</governor>
            				<dependent idx="4">,</dependent>
          			</dep>
          			<dep type="cc">
            				<governor idx="3">abc</governor>
            				<dependent idx="5">and</dependent>
          			</dep>
          			<dep type="nsubj">
            				<governor idx="9">def</governor>
            				<dependent idx="6">it</dependent>
          			</dep>
          			<dep type="cop">
            				<governor idx="9">def</governor>
            				<dependent idx="7">is</dependent>
          			</dep>
          			<dep type="neg">
            				<governor idx="9">def</governor>
            				<dependent idx="8">not</dependent>
          			</dep>
          			<dep type="conj:and">
            				<governor idx="3">abc</governor>
            				<dependent idx="9">def</dependent>
          			</dep>
        		</dependencies>
        		<dependencies type="collapsed-ccprocessed-dependencies">
          			<dep type="root">
            				<governor idx="0">ROOT</governor>
            				<dependent idx="3">abc</dependent>
          			</dep>
          			<dep type="nsubj">
            				<governor idx="3">abc</governor>
            				<dependent idx="1">abc</dependent>
          			</dep>
          			<dep type="cop">
            				<governor idx="3">abc</governor>
            				<dependent idx="2">is</dependent>
          			</dep>
          			<dep type="punct">
            				<governor idx="3">abc</governor>
            				<dependent idx="4">,</dependent>
          			</dep>
          			<dep type="cc">
            				<governor idx="3">abc</governor>
            				<dependent idx="5">and</dependent>
          			</dep>
          			<dep type="nsubj">
            				<governor idx="9">def</governor>
            				<dependent idx="6">it</dependent>
          			</dep>
          			<dep type="cop">
            				<governor idx="9">def</governor>
            				<dependent idx="7">is</dependent>
          			</dep>
          			<dep type="neg">
            				<governor idx="9">def</governor>
            				<dependent idx="8">not</dependent>
          			</dep>
          			<dep type="conj:and">
            				<governor idx="3">abc</governor>
            				<dependent idx="9">def</dependent>
          			</dep>
        		</dependencies>
        		<dependencies type="enhanced-dependencies">
          			<dep type="root">
            				<governor idx="0">ROOT</governor>
            				<dependent idx="3">abc</dependent>
          			</dep>
          			<dep type="nsubj">
            				<governor idx="3">abc</governor>
            				<dependent idx="1">abc</dependent>
          			</dep>
          			<dep type="cop">
            				<governor idx="3">abc</governor>
            				<dependent idx="2">is</dependent>
          			</dep>
          			<dep type="punct">
            				<governor idx="3">abc</governor>
            				<dependent idx="4">,</dependent>
          			</dep>
          			<dep type="cc">
            				<governor idx="3">abc</governor>
            				<dependent idx="5">and</dependent>
          			</dep>
          			<dep type="nsubj">
            				<governor idx="9">def</governor>
            				<dependent idx="6">it</dependent>
          			</dep>
          			<dep type="cop">
            				<governor idx="9">def</governor>
            				<dependent idx="7">is</dependent>
          			</dep>
          			<dep type="neg">
            				<governor idx="9">def</governor>
            				<dependent idx="8">not</dependent>
          			</dep>
          			<dep type="conj:and">
            				<governor idx="3">abc</governor>
            				<dependent idx="9">def</dependent>
          			</dep>
        		</dependencies>
        		<dependencies type="enhanced-plus-plus-dependencies">
          			<dep type="root">
            				<governor idx="0">ROOT</governor>
            				<dependent idx="3">abc</dependent>
          			</dep>
          			<dep type="nsubj">
            				<governor idx="3">abc</governor>
            				<dependent idx="1">abc</dependent>
          			</dep>
          			<dep type="cop">
            				<governor idx="3">abc</governor>
            				<dependent idx="2">is</dependent>
          			</dep>
          			<dep type="punct">
            				<governor idx="3">abc</governor>
            				<dependent idx="4">,</dependent>
          			</dep>
          			<dep type="cc">
            				<governor idx="3">abc</governor>
            				<dependent idx="5">and</dependent>
          			</dep>
          			<dep type="nsubj">
            				<governor idx="9">def</governor>
            				<dependent idx="6">it</dependent>
          			</dep>
          			<dep type="cop">
            				<governor idx="9">def</governor>
            				<dependent idx="7">is</dependent>
          			</dep>
          			<dep type="neg">
            				<governor idx="9">def</governor>
            				<dependent idx="8">not</dependent>
          			</dep>
          			<dep type="conj:and">
            				<governor idx="3">abc</governor>
            				<dependent idx="9">def</dependent>
          			</dep>
        		</dependencies>
      	</sentence>
    </sentences>
'''