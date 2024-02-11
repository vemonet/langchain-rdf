from langchain_rdf import OntologyLoader, __version__


def test_ontology_loader_sio():
    """Test the package main function"""
    loader = OntologyLoader("https://semanticscience.org/ontology/sio.owl", format="xml")
    documents = loader.load()
    print(documents)
    assert len(documents) >= 10


def test_version():
    """Test the version is a string."""
    assert isinstance(__version__, str)
