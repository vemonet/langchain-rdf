from langchain_rdf import OntologyLoader, SparqlExamplesLoader, __version__


def test_ontology_loader_sio():
    """Test the ontology loader with the SIO ontology."""
    loader = OntologyLoader("https://semanticscience.org/ontology/sio.owl", format="xml")
    documents = loader.load()
    # print(documents)
    assert len(documents) >= 10


def test_sparql_examples_loader_uniprot():
    """Test the SPARQL queries examples loader with the UniProt endpoint."""
    loader = SparqlExamplesLoader("https://sparql.uniprot.org/sparql/")
    documents = loader.load()
    print(documents)
    assert len(documents) >= 10


def test_sparql_examples_loader_error_nextprot():
    """Test the SPARQL queries examples loader with the UniProt endpoint."""
    try:
        _loader = SparqlExamplesLoader("https://sparql.nextprot.org/")
        raise AssertionError("Should have raised an error")
    except ValueError as e:
        assert "Could not query the provided endpoint at" in str(e)


def test_version():
    """Test the version is a string."""
    assert isinstance(__version__, str)
