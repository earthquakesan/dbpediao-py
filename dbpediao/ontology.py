import RDF
import os

class OntologyReasoner(object):
    rdfs_subClassOf = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
    bottomConcepts = set()

    def __init__(self):
        self.model = self._initOntology()
        pass

    def _initOntology(self):
        storage = RDF.HashStorage('dbpedia', options="hash-type='bdb'")
        model = RDF.Model(storage)
        rdfParser = RDF.Parser(name="rdfxml")
        ontologyPath = 'file://' + os.path.join(self._getCurrentDir(), 'dbpedia_3.9.owl')
        rdfParser.parse_into_model(model, ontologyPath,  "http://example.org/")
        return model

    def _getCurrentDir(self):
        return os.path.dirname(os.path.realpath(__file__))

    def findBottomConcept(self, concepts):
        print concepts
        if(not concepts): #concepts are empty
            return ''
        result = []
        for concept in self._sortConceptsByHierarchy(concepts):
            if(concept[0] == 0):
                result.append(concept[1])
        return result[0]

    def _sortConceptsByHierarchy(self, concepts):
        concepts = set(concepts)
        conceptsHierarchy = []
        for concept in concepts:
            bottomConcepts = self._findBottomConcepts(concept)
            bottomInConcepts = self.bottomConcepts.intersection(concepts)
            rank = len(bottomInConcepts)
            conceptsHierarchy.append( (rank, concept) )
            self.bottomConcepts = set()

        return sorted(conceptsHierarchy)

    def _findBottomConcepts(self, conceptUri):
        qs = RDF.Statement(subject = None,
                           predicate = RDF.Node(uri_string = self.rdfs_subClassOf),
                           object = RDF.Node(uri_string = str(conceptUri)))
        for statement in self.model.find_statements(qs):
            bottomConcept = str(statement.subject.uri)
            self.bottomConcepts.add(bottomConcept)
            if(statement):
                self._findBottomConcepts(bottomConcept)

if __name__ == "__main__":
    myset = eval("""[u'http://dbpedia.org/ontology/Country',
            u'http://dbpedia.org/ontology/Place',
            u'http://dbpedia.org/ontology/PopulatedPlace']""")
    #myset = eval("""[u'http://dbpedia.org/class/yago/Abstraction100002137',
    #        u'http://dbpedia.org/class/yago/AdministrativeDistrict108491826',
    #        u'http://dbpedia.org/class/yago/CountriesBorderingTheAtlanticOcean',
    #        u'http://dbpedia.org/class/yago/Country108544813',
    #        u'http://dbpedia.org/class/yago/District108552138']""")
    ontologyReasoner = OntologyReasoner()
    print ontologyReasoner.findBottomConcept(myset)
