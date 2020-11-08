


from spacy.lang.de import German
import spacy
from spacy.lang.en import English
import networkx as nx
import matplotlib.pyplot as plt

def getSentences(text):
    nlp = German()
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    document = nlp(text)
    return [sent.string.strip() for sent in document.sents]

def printToken(token):
    print(token.text, "->", token.dep_)

def appendChunk(original, chunk):
    return original + ' ' + chunk

def isRelationCandidate(token):
    deps = ["ROOT","svp"]
    #deps = ["ROOT", "adj", "attr", "agent", "amod"]
    return any(subs in token.dep_ for subs in deps)

def isConstructionCandidate(token):
    #deps = ["adc"]
    deps = ["op","nk"]
    #deps = ["compound", "prep", "conj", "mod"] 
    #2 zusammen gesetze wörter, 
    return any(subs in token.dep_ for subs in deps)

def processSubjectObjectPairs(tokens):
    subject = ''
    object = ''
    relation = ''
    subjectConstruction = ''
    objectConstruction = ''
    for token in tokens:
        printToken(token)
        if "punct" in token.dep_:
            continue
        if isRelationCandidate(token):
            relation = appendChunk(relation, token.lemma_)
        if isConstructionCandidate(token):
            if subjectConstruction:
                subjectConstruction = appendChunk(subjectConstruction, token.text)
            if objectConstruction:
                objectConstruction = appendChunk(objectConstruction, token.text)
        if "ag" in token.dep_:
            subject = appendChunk(subject, token.text)
            subject = appendChunk(subjectConstruction, subject)
            subjectConstruction = ''
        if "oa" in token.dep_:
            object = appendChunk(object, token.text)
            object = appendChunk(objectConstruction, object)
            objectConstruction = ''
        if "sb" in token.dep_:
            object = appendChunk(object, token.text)
            object = appendChunk(objectConstruction, object)
            objectConstruction = ''    

    print (subject.strip(), ",", relation.strip(), ",", object.strip())
    return (subject.strip(), relation.strip(), object.strip())

def processSentence(sentence):
    tokens = nlp_model(sentence)
    return processSubjectObjectPairs(tokens)

def printGraph(triples):
    G = nx.Graph()
    for triple in triples:
        G.add_node(triple[0])
        G.add_node(triple[1])
        G.add_node(triple[2])
        G.add_edge(triple[0], triple[1])
        G.add_edge(triple[1], triple[2])

    pos = nx.spring_layout(G)
    plt.figure()
    nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='seagreen', alpha=0.9,
            labels={node: node for node in G.nodes()})
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    #plt.rcParams['interactive'] == True
    text= "Kundenkommunikation Der Umgang zur Kommunikation ist eine zentrale Voraussetzung der Dienstleistung, um die Kundenzufriedenheit zu gewährleisten. Die Kommunikationswege des von MiQ sollten für alle Kunden zur Verfügung stehen und auffindbar sein. Über die Webseite besteht die Möglichkeit MiQ über E-Mail, Telefon oder vor Ort an zu treffen. Die Verantwortung über die Kommunikation mit dem Kunden trägt dabei das Qualitätsmanagement (QM). Der Umgang mit dem Kunden führt nach der ersten erfolgreichen Kontaktaufnahme, meistens zu einem persönlichem Gespräch. In diesem Gespräch werden Rahmenbedingungen für das weitere Vorgehen festgelegt und Kundenanforderungen sowie die eigene Leistungsfähigkeit besprochen. Im Falle der Dienstleistungstätigkeiten wird das Dokument zur Beauftragung des Kunden herangezogen, um das Aufgabengebiet von MiQ schriftlich festzuhalten. Teil der Kundenkommunikation ist die Kundenzufriedenheit. Diese wird entsprechend der Richtlinie in regelmäßigen Abständen analysiert, um die Kundenanforderungen und wünsche laufend zu überwachen. Kundeneigentum Als Dienstleister gehen wir mit Kundeneigentum, insbesondere mit dem geistigen Eigentum unserer Kunden, sorgsam um. Alle Daten werden anhand entsprechender Gesetze geschützt und durch Datenverlust gesichert. Der komplexe Aufbau der Serverstruktur von Qsistant ermöglicht uns, jeden Kunden eine anonyme und abgekapselte Arbeitsumgebung zu schaffen. Verträge, Angebote und andere ausgedruckte kundenspezifische Unterlagen werden in einem Ordner und abgeschlossen aufbewahrt, um den Zugriff durch Dritte zu verhindern."
    sentences = getSentences(text)
    nlp_model = spacy.load('de_core_news_lg')

    triples = []
    print (text)
    for sentence in sentences:
        triples.append(processSentence(sentence))

    printGraph(triples)



