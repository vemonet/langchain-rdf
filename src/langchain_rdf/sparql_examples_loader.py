import re
from typing import Any, Dict, List

from langchain_core.document_loaders.base import BaseLoader
from langchain_core.documents import Document
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery
from rdflib.plugins.stores import sparqlstore


class SparqlExamplesLoader(BaseLoader):
    """
    Load SPARQL queries examples from a SPARQL endpoint stored using the SHACL ontology as documents.
    """

    def __init__(self, endpoint_url: str):
        """
        Initialize the SparqlExamplesLoader.

        Args:
            sparql_endpoint (str): URL of the SPARQL endpoint to retrieve SPARQL queries from.
        """
        self.endpoint_url = endpoint_url
        store = sparqlstore.SPARQLStore(query_endpoint=endpoint_url, auth=None)
        self.graph = Graph(store, identifier=None, bind_namespaces="none")
        self.atag_pattern = re.compile(r"<a\b[^>]*>(.*?)<\/a>", re.IGNORECASE)
        try:
            self.graph.query("ASK { ?s ?p ?o }")
        except ValueError as e:
            raise ValueError(f"Could not query the provided endpoint at {endpoint_url}: {e}") from e

    def load(self) -> List[Document]:
        """Load and return documents (classes and properties) from the SPARQL endpoint."""
        # Extract classes and properties as documents
        docs: List[Document] = []

        # Get prefixes
        prefix_map: Dict[str, str] = {}
        row: Any
        for row in self.graph.query(self._get_prefixes_query()):
            prefix_map[str(row.prefix)] = str(row.namespace)

        for row in self.graph.query(self._get_sparql_examples_query()):
            docs.append(self._create_document(row, prefix_map))
        return docs

    def _create_document(self, row: Any, prefix_map: Dict[str, str]) -> Document:
        """Create a Document object from a query result row."""
        query = self._remove_a_tags(str(row.query))
        comment = str(row.comment)
        # Add prefixes to query if not already present
        for prefix, namespace in prefix_map.items():
            prefix_str = f"PREFIX {prefix}: <{namespace}>"
            if not re.search(prefix_str, query) and re.search(f"[(| |\u00a0|/]{prefix}:", query):
                query = f"{prefix_str}\n{query}"
        parsed_query = prepareQuery(query)
        return Document(
            page_content=comment,
            metadata={
                "comment": comment,
                "query": query,
                "endpoint_url": self.endpoint_url,
                "query_type": parsed_query.algebra.name,
            },
        )

    def _get_sparql_examples_query(self) -> str:
        """Query to extract SPARQL query examples"""
        return """PREFIX sh: <http://www.w3.org/ns/shacl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?comment ?query
WHERE {
    ?sq a sh:SPARQLExecutable ;
        rdfs:label|rdfs:comment ?comment ;
        sh:select|sh:ask|sh:construct|sh:describe ?query .
}"""

    def _get_prefixes_query(self) -> str:
        """Query to extract prefixes"""
        return """PREFIX sh: <http://www.w3.org/ns/shacl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prefix ?namespace
WHERE {
    [] sh:namespace ?namespace ;
        sh:prefix ?prefix .
} ORDER BY ?prefix"""

    def _remove_a_tags(self, text: str) -> str:
        """Remove <a> tags from a string."""
        # Use re.sub to replace the <a> tags with the content inside them
        return re.sub(self.atag_pattern, r"\1", text)
