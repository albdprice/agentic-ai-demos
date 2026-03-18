"""
Tool implementations for the drug discovery agent.
PubChem and Semantic Scholar are free, public APIs - no keys needed.
"""
import json
import urllib.request
import urllib.parse
from typing import Optional

def pubchem_search(compound_name: str) -> dict:
    """
    Query PubChem for molecular properties.
    Returns molecular formula, weight, SMILES, IUPAC name, and key identifiers.
    """
    base = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    try:
        # Get CID from name
        url = f"{base}/compound/name/{urllib.parse.quote(compound_name)}/property/MolecularFormula,MolecularWeight,CanonicalSMILES,IUPACName,XLogP,TPSA,HBondDonorCount,HBondAcceptorCount/JSON"
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read())
        
        props = data["PropertyTable"]["Properties"][0]
        return {
            "compound": compound_name,
            "cid": props.get("CID"),
            "formula": props.get("MolecularFormula"),
            "molecular_weight": props.get("MolecularWeight"),
            "smiles": props.get("CanonicalSMILES"),
            "iupac_name": props.get("IUPACName"),
            "logp": props.get("XLogP"),
            "tpsa": props.get("TPSA"),
            "hbd": props.get("HBondDonorCount"),
            "hba": props.get("HBondAcceptorCount"),
            "source": "PubChem"
        }
    except Exception as e:
        return {"compound": compound_name, "error": str(e)}


def literature_search(query: str, limit: int = 5) -> list:
    """
    Search Semantic Scholar for relevant papers.
    Returns titles, authors, abstracts, citation counts, and DOIs.
    """
    base = "https://api.semanticscholar.org/graph/v1"
    try:
        params = urllib.parse.urlencode({
            "query": query,
            "limit": limit,
            "fields": "title,authors,abstract,citationCount,year,externalIds"
        })
        url = f"{base}/paper/search?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": "DrugDiscoveryAgent/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        
        papers = []
        for p in data.get("data", []):
            papers.append({
                "title": p.get("title"),
                "authors": [a.get("name", "") for a in p.get("authors", [])[:3]],
                "year": p.get("year"),
                "citations": p.get("citationCount", 0),
                "abstract": (p.get("abstract") or "")[:300],
                "doi": p.get("externalIds", {}).get("DOI"),
            })
        return papers
    except Exception as e:
        return [{"error": str(e)}]


if __name__ == "__main__":
    # Quick test
    print("=== PubChem: Aspirin ===")
    result = pubchem_search("aspirin")
    for k, v in result.items():
        print(f"  {k}: {v}")
    
    print("\n=== Literature: DFT dispersion corrections ===")
    papers = literature_search("density functional theory dispersion corrections", limit=3)
    for p in papers:
        print(f"  [{p.get(year)}] {p.get(title)} (cited: {p.get(citations)})")
