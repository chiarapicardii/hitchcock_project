from lxml import etree
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD
import re

TEI_NS = "http://www.tei-c.org/ns/1.0"
PSYCHO = Namespace("http://example.org/psycho/schema#")
RESOURCE = Namespace("http://example.org/psycho/resource/")

# Namespace per lxml XPath
NSMAP = {'tei': TEI_NS}

g = Graph()
g.bind("psycho", PSYCHO )
g.bind("resource", RESOURCE)
g.bind("rdfs", RDFS)
g.bind("xsd", XSD)

# creo URI "slugificati"
def slugify(text):
    text = re.sub(r'\W+', '_', text) # Sostituisce caratteri non alfanumerici con _
    return text.strip('_').lower()

tree = etree.parse("Psycho TEI.xml") 
root = tree.getroot()


# URI del film
movie_uri = RESOURCE.movie

# Aggiungo il tipo per il film
g.add((movie_uri, RDF.type, PSYCHO.Movie))

# Estraggo il titolo
title_element = root.find('.//tei:titleStmt/tei:title', namespaces=NSMAP)
if title_element is not None and title_element.text:
    movie_title = title_element.text
    g.add((movie_uri, PSYCHO.hasTitle, Literal(movie_title)))
    g.add((movie_uri, RDFS.label, Literal(movie_title))) # Anche un label generico

# Estraggo durata film
extent_element = root.find('.//tei:fileDesc/tei:extent[@unit="minutes"]', namespaces=NSMAP)
if extent_element is not None and extent_element.text:
    try:
        duration = int(extent_element.text)
        g.add((movie_uri, PSYCHO.hasDurationMinutes, Literal(duration, datatype=XSD.integer)))
    except ValueError:
        print(f"Attenzione: Valore durata non valido: {extent_element.text}")


# estraggo anno di pubblicazione
pub_date_element = root.find('.//tei:publicationStmt/tei:date', namespaces=NSMAP)
if pub_date_element is not None and pub_date_element.text:
    try:
        pub_year = int(pub_date_element.text)
        g.add((movie_uri, PSYCHO.hasPublicationYear, Literal(pub_year, datatype=XSD.gYear)))
    except ValueError:
        print(f"Attenzione: Valore anno di pubblicazione non valido: {pub_date_element.text}")
       
resp_stmts = root.findall('.//tei:titleStmt/tei:respStmt', namespaces=NSMAP)
for resp_stmt in resp_stmts:
    resp_text_element = resp_stmt.find('tei:resp', namespaces=NSMAP)
    if resp_text_element is None or not resp_text_element.text:
        continue
    
    role_text = resp_text_element.text.strip()
    # Normalizzo il testo del ruolo per usarlo come parte del nome della proprietà
    # es. "Director of Photography" diventa "hasDirectorOfPhotography"
    prop_name_suffix = ''.join(word.capitalize() for word in re.split(r'\W+', role_text) if word)
    role_prop_uri = PSYCHO[f"has{prop_name_suffix}"] # Proprietà dinamica tipo ex:hasDirector

    names_elements = resp_stmt.findall('tei:name', namespaces=NSMAP)
    for name_element in names_elements:
        if name_element.text:
            person_name = name_element.text.strip()
            person_slug = slugify(person_name)
            person_uri = RESOURCE[f"person/{person_slug}"]

            g.add((person_uri, RDF.type, PSYCHO.Person))
            g.add((person_uri, RDFS.label, Literal(person_name)))
            g.add((movie_uri, role_prop_uri, person_uri))

            cast_items = root.findall('.//tei:front/tei:castList/tei:castItem', namespaces=NSMAP)
for item in cast_items:
    actor_name_element = item.find('tei:actor', namespaces=NSMAP)
    role_name_element = item.find('tei:roleName', namespaces=NSMAP)

    if actor_name_element is not None and actor_name_element.text and \
       role_name_element is not None and role_name_element.text:
        
        actor_name = actor_name_element.text.strip()
        actor_slug = slugify(actor_name)
        actor_uri = RESOURCE[f"person/{actor_slug}"] 

        # Aggiungo tipo e label per l'attore se non già fatto
        # rdflib gestisce i duplicati.
        g.add((actor_uri, RDF.type, PSYCHO.Person))
        g.add((actor_uri, RDFS.label, Literal(actor_name)))
        
        # Collego il film all'attore
        g.add((movie_uri, PSYCHO.hasCastMember, actor_uri))

        character_name = role_name_element.text.strip()
        # Controllo se esiste un attributo 'alt' per il personaggio
        alt_name_element = role_name_element.get('alt')
        if alt_name_element: # Se c'è un nome alternativo, uso quello come label principale se diverso
            main_char_name_for_label = character_name
            char_slug = slugify(main_char_name_for_label) 
        else:
            main_char_name_for_label = character_name
            char_slug = slugify(character_name)

        character_uri = RESOURCE[f"character/{char_slug}"]
        
        g.add((character_uri, RDF.type, PSYCHO.Character))
        g.add((character_uri, RDFS.label, Literal(main_char_name_for_label)))
        if alt_name_element and alt_name_element != main_char_name_for_label : # Se 'alt' è presente e diverso
             g.add((character_uri, PSYCHO.hasAlternativeName, Literal(alt_name_element)))


        # Collego l'attore al personaggio
        g.add((actor_uri, PSYCHO.playsCharacter, character_uri))

        
output_file = "psycho_tei.ttl"
try:
    g.serialize(destination=output_file, format="turtle")
    print(f"Grafo RDF salvato in {output_file}")
except Exception as e:
    print(f"Errore durante la serializzazione del grafo: {e}")
