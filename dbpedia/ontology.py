import RDF
import os

class OntologyReasoner(object):
    rdfs_subClassOf = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
    bottomConcepts = set()

    def __init__(self):
        self.model = self.initOntology()
        pass

    def initOntology(self):
        storage = RDF.HashStorage('dbpedia', options="hash-type='bdb'")
        model = RDF.Model(storage)
        rdfParser = RDF.Parser(name="rdfxml")
        ontologyPath = 'file://' + os.path.join(self.getCurrentDir(), 'dbpedia_3.9.owl')
        rdfParser.parse_into_model(model, ontologyPath,  "http://example.org/")
        return model

    def getCurrentDir(self):
        return os.path.dirname(os.path.realpath(__file__))

    def findBottomConcept(self, concepts):
        return self.sortConceptsByHierarchy(concepts)[0][1]

    def sortConceptsByHierarchy(self, concepts):
        concepts = set(concepts)
        conceptsHierarchy = []
        for concept in concepts:
            bottomConcepts = self.findBottomConcepts(concept)
            bottomInConcepts = self.bottomConcepts.intersection(concepts)
            rank = len(bottomInConcepts)
            conceptsHierarchy.append( (rank, concept) )
            self.bottomConcepts = set()

        return sorted(conceptsHierarchy)

    def findBottomConcepts(self, conceptUri):
        qs = RDF.Statement(subject = None,
                           predicate = RDF.Node(uri_string = self.rdfs_subClassOf),
                           object = RDF.Node(uri_string = conceptUri))
        for statement in self.model.find_statements(qs):
            bottomConcept = str(statement.subject.uri)
            self.bottomConcepts.add(bottomConcept)
            if(statement):
                self.findBottomConcepts(bottomConcept)

if __name__ == "__main__":
    testConcept = ["http://dbpedia.org/ontology/Country"]
    testConcept.append("http://dbpedia.org/ontology/PopulatedPlace")
    testConcept.append("http://dbpedia.org/ontology/Place")
    ontologyReasoner = OntologyReasoner()
    print ontologyReasoner.findBottomConcept(testConcept)
    import ipdb; ipdb.set_trace()
    print "hi"
