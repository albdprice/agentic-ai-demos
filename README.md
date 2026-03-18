# Agentic AI Demos for Scientific Research

Autonomous AI agent systems for drug discovery, clinical data analysis, and scientific literature research. Built with LangChain/LangGraph, demonstrating multi-agent architectures with tool use, memory systems, and RAG pipelines.

## Demos

### 1. Drug Discovery Agent (`drug_discovery_agent/`)
A LangGraph multi-agent system that:
- Searches PubChem for molecular properties and bioactivity data
- Queries scientific literature via Semantic Scholar API
- Runs molecular property predictions using MACE ML potentials
- Generates structured research reports with citations

### 2. Clinical Data Agent (`clinical_data_agent/`)
RAG-powered agent for clinical trial data analysis:
- Ingests clinical trial protocols and results (PDF/structured data)
- Answers questions about trial design, endpoints, and outcomes
- Compares across trials using vector similarity search
- Generates summary reports for stakeholders

### 3. Molecular Literature RAG (`molecular_rag/`)
Retrieval-augmented generation for computational chemistry papers:
- PDF ingestion with chemical-aware parsing
- Vector store with molecular structure embeddings
- Question answering grounded in source papers
- BibTeX generation from retrieved sources

## Architecture

```
User Query → Planning Agent → Tool Selection
                ↓
    ┌───────────┼───────────┐
    ↓           ↓           ↓
  PubChem    Literature   ML Model
  Agent      Agent        Agent
    ↓           ↓           ↓
    └───────────┼───────────┘
                ↓
        Synthesis Agent → Report
```

## Tech Stack

- **Orchestration**: LangGraph (stateful multi-agent graphs)
- **LLM**: Claude (Anthropic API) / Ollama (local, GPU-accelerated)
- **Vector DB**: ChromaDB
- **ML**: MACE neural network potentials, ASE
- **APIs**: PubChem PUG REST, Semantic Scholar, CrossRef

## Setup

```bash
pip install langchain langgraph langchain-anthropic chromadb
pip install mace-torch ase  # for molecular predictions
export ANTHROPIC_API_KEY=your_key
```

## Related

- [molecular-ml-pipeline](https://github.com/albdprice/molecular-ml-pipeline) — MACE training pipeline
- [adaptive-ml-potentials](https://github.com/albdprice/adaptive-ml-potentials) — Physics-informed ML
