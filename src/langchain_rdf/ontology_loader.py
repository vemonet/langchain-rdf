from typing import Any, List, Optional

from langchain_community.document_loaders.base import BaseLoader
from langchain_core.documents import Document
from rdflib import Graph


class OntologyLoader(BaseLoader):
    """
    Load an OWL ontology and extract classes and properties as documents.
    """

    def __init__(self, ontology_url: str, format: Optional[str] = None):
        """
        Initialize the OntologyLoader.

        Args:
            ontology_url (str): URL of the OWL ontology to be loaded.
            format (str): FOrmat of the OWL ontology to be loaded.
        """
        self.ontology_url = ontology_url
        self.format = format
        self.graph = Graph(store="Oxigraph")
        self.graph.parse(self.ontology_url, format=self.format)

    def load(self) -> List[Document]:
        """Load and return documents (classes and properties) from the OWL ontology."""
        # Extract classes and properties as documents
        docs: List[Document] = []
        for cls in self.graph.query(self._get_class_query()):
            docs.append(self._create_document(cls))
        for prop in self.graph.query(self._get_property_query()):
            docs.append(self._create_document(prop))
        return docs

    def _create_document(self, result_row: Any) -> Document:
        """Create a Document object from a query result row."""
        label = str(result_row.label)
        return Document(
            page_content=label,
            metadata={
                "label": label,
                "uri": str(result_row.uri),
                "type": str(result_row.type),
                "predicate": str(result_row.pred),
                "ontology": self.ontology_url,
            },
        )

    def _get_class_query(self) -> str:
        """Query to extract class labels"""
        return """PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX owl:  <http://www.w3.org/2002/07/owl#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            PREFIX dcterms: <http://purl.org/dc/terms/>

            SELECT ?uri ?pred ?label ?type
            WHERE {
                ?uri a ?type ;
                    ?pred ?label .
                FILTER (
                    ?type = owl:Class
                )
                FILTER (
                    ?pred = rdfs:label ||
                    ?pred = skos:prefLabel ||
                    ?pred = skos:altLabel ||
                    ?pred = skos:definition ||
                    ?pred = rdfs:comment ||
                    ?pred = dcterms:description ||
                    ?pred = dc:title
                )
            }
        """

    def _get_property_query(self) -> str:
        """Query to extract property labels"""
        return """PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX owl:  <http://www.w3.org/2002/07/owl#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            PREFIX dcterms: <http://purl.org/dc/terms/>

            SELECT ?uri ?pred ?label ?type
            WHERE {
                ?uri a ?type ;
                    ?pred ?label .
                FILTER (
                    ?type = owl:DatatypeProperty ||
                    ?type = owl:ObjectProperty
                )
                FILTER (
                    ?pred = rdfs:label ||
                    ?pred = skos:prefLabel ||
                    ?pred = skos:altLabel ||
                    ?pred = skos:definition ||
                    ?pred = rdfs:comment ||
                    ?pred = dcterms:description ||
                    ?pred = dc:title
                )
            }
        """
