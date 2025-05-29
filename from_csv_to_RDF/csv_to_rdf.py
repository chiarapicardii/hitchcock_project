import csv
from urllib.parse import quote #because I was having problems encoding the URI 
from rdflib import Graph, Literal, URIRef, Namespace

def csv_to_rdf(csv_file, graph):

    #namespaces 
    dcterms = Namespace("http://purl.org/dc/terms/")
    schema = Namespace("https://schema.org/")
    foaf = Namespace("http://xmlns.com/foaf/0.1/")
    wd = Namespace("https://www.wikidata.org/wiki/")
    getty = Namespace("http://vocab.getty.edu/aat/")
    loc_class = Namespace("https://id.loc.gov/authorities/classification/")
    loc_subj = Namespace("https://id.loc.gov/authorities/subjects/")
    frbr = Namespace("http://iflastandards.info/ns/fr/frbr/frbrer/")
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    skos = Namespace("http://www.w3.org/2004/02/skos/core#")
    local = Namespace("https://chiarapicardii.github.io/hitchcock_project/")
    viaf = Namespace("https://viaf.org/viaf/")

    #connecting them to the graph 
    graph.bind("dcterms", dcterms)
    graph.bind("schema", schema)
    graph.bind("foaf", foaf)
    graph.bind("wd", wd)
    graph.bind("getty", getty)
    graph.bind("loc_subj", loc_subj)
    graph.bind("loc_class", loc_class)
    graph.bind("frbr", frbr)
    graph.bind("rdf", rdf)
    graph.bind("skos", skos)
    graph.bind("viaf", viaf)
    graph.bind("local", local)

    #reading the csv 
    with open(csv_file, "r", encoding="utf-8") as f: 
        reader = csv.DictReader(f)
        for row in reader: 
            csv_subj = row["Subject"].strip() #normalizing and deleting whitespases 
            csv_pred = row["Predicate"].strip()
            csv_obj = row["Object"].strip()

            #problem:some items have an URI some others don't so i have to check and in case create a new one 
            if csv_subj.startswith("http") or csv_subj.startswith("https"): 
                subj = URIRef(csv_subj)
            else: 
                subj = URIRef(str(local) + quote(csv_subj))

            #all the predicates have a precise uri so I just need to transformit it in an URI 
            if csv_pred:
                pred = URIRef(csv_pred) 

            #for the object, the one who aren't associated with an URI are transformed in a Literal 
            if csv_obj.startswith("http") or csv_obj.startswith("https"): 
                obj = URIRef(csv_obj)
            else: 
                obj = Literal(csv_obj)

            #adding the triple to the graph 
            graph.add((subj, pred, obj))   

#initializing a graph outside the loop so it will keep the results
graph = Graph()

#all the files to process
all_csv_file = [
    "alfred_hitchcock_on_dead_bodies_2017.csv",
    "alfred_hitchcock_presents_signatures_in_suspense_1999.csv",
    "bakers_dozen_suspense_stories_1963.csv",
    "frbr_Psycho_and_Lifeboat.csv",
    "hitchcock_psycho_shower_scene_1960.csv",
    "psycho_movie_poster_1960.csv",
    "psycho_screenplay_1960.csv",
    "psycho_theatrical_trailer_1960.csv",
    "storyboard_lifeboat_1944.csv",
    "suspense_thriller_film_shadow_hitchcock_1951.csv",
    "truffaut_hitchcock_1966.csv"
]

#itarating through the list and taking one item at a time, then appening it to the graph 
for csv_file in all_csv_file: 
    csv_to_rdf(csv_file, graph)

#serializing the result 
try: 
    graph.serialize(destination="csv_to_rdf.ttl", format="turtle")
    print("RDF correctly saved in the output.ttl file")

except Exception as e:
    print("Something went wrong with the serialization:" + str(e))
