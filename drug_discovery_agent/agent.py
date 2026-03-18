"""
Drug Discovery Agent
====================
Multi-agent system for molecular property lookup and literature analysis.
Uses PubChem and Semantic Scholar APIs with LLM synthesis via Ollama or Claude.

Architecture:
    Query -> Planner -> [PubChem Agent, Literature Agent] -> Synthesizer -> Report
"""
import json
from typing import TypedDict, Annotated
from tools import pubchem_search, literature_search

try:
    from langgraph.graph import StateGraph, END
    HAS_LANGGRAPH = True
except ImportError:
    HAS_LANGGRAPH = False
    print("langgraph not installed - running in standalone mode")

try:
    import urllib.request
    def query_ollama(prompt, model="qwen2.5:7b", url="http://10.10.49.9:11434"):
        """Query the local Ollama instance for LLM synthesis."""
        data = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode()
        req = urllib.request.Request(f"{url}/api/generate", data=data,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())["response"]
except Exception:
    def query_ollama(prompt, **kwargs):
        return "[LLM not available - showing raw data]"


class AgentState(TypedDict):
    query: str
    compound_data: dict
    literature: list
    synthesis: str


def plan_node(state: AgentState) -> dict:
    """Extract the compound name and research question from the query."""
    return state


def pubchem_node(state: AgentState) -> dict:
    """Look up molecular properties from PubChem."""
    query = state["query"]
    # Simple extraction: use the first noun-like word as the compound
    compound = query.split("about ")[-1].split("?")[0].split(" properties")[0].strip()
    data = pubchem_search(compound)
    return {"compound_data": data}


def literature_node(state: AgentState) -> dict:
    """Search for relevant scientific literature."""
    query = state["query"]
    papers = literature_search(query, limit=5)
    return {"literature": papers}


def synthesis_node(state: AgentState) -> dict:
    """Synthesize findings into a structured report."""
    compound = state.get("compound_data", {})
    papers = state.get("literature", [])
    
    prompt = f"""Based on the following data, write a brief research summary:

Molecular Properties:
{json.dumps(compound, indent=2)}

Relevant Literature:
{json.dumps(papers, indent=2)}

Write a 3-paragraph summary covering: (1) molecular properties and drug-likeness, 
(2) key findings from the literature, (3) potential research directions."""

    synthesis = query_ollama(prompt)
    return {"synthesis": synthesis}


def run_agent(query: str) -> dict:
    """Run the drug discovery agent on a query."""
    if HAS_LANGGRAPH:
        # Build the state graph
        workflow = StateGraph(AgentState)
        workflow.add_node("plan", plan_node)
        workflow.add_node("pubchem", pubchem_node)
        workflow.add_node("literature", literature_node)
        workflow.add_node("synthesize", synthesis_node)
        
        workflow.set_entry_point("plan")
        workflow.add_edge("plan", "pubchem")
        workflow.add_edge("plan", "literature")
        workflow.add_edge("pubchem", "synthesize")
        workflow.add_edge("literature", "synthesize")
        workflow.add_edge("synthesize", END)
        
        app = workflow.compile()
        result = app.invoke({"query": query, "compound_data": {}, "literature": [], "synthesis": ""})
        return result
    else:
        # Standalone mode without langgraph
        print(f"Query: {query}")
        compound = query.split("about ")[-1].split("?")[0].split(" properties")[0].strip()
        
        print(f"\n--- PubChem: {compound} ---")
        compound_data = pubchem_search(compound)
        for k, v in compound_data.items():
            print(f"  {k}: {v}")
        
        print(f"\n--- Literature ---")
        papers = literature_search(query, limit=3)
        for p in papers:
            if "error" not in p:
                print(f"  [{p.get(year)}] {p.get(title)} (cited: {p.get(citations)})")
        
        print(f"\n--- Synthesis ---")
        synthesis = synthesis_node({"query": query, "compound_data": compound_data, "literature": papers})
        print(synthesis.get("synthesis", ""))
        
        return {"compound_data": compound_data, "literature": papers, "synthesis": synthesis}


if __name__ == "__main__":
    result = run_agent("What are the properties and recent research about ibuprofen?")
