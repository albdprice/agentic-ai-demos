# Agentic AI for Scientific Research

Multi-agent AI systems for drug discovery, clinical data analysis, and scientific literature research. These are working prototypes exploring how autonomous agents can accelerate computational chemistry workflows.

## Projects

### Drug Discovery Agent
A LangGraph multi-agent system that queries PubChem for molecular properties, searches literature via Semantic Scholar, runs property predictions with MACE potentials, and synthesizes findings into structured reports. The architecture separates planning, tool execution, and synthesis into distinct agents with shared memory.

### Clinical Data Agent
RAG pipeline for clinical trial data. Ingests protocols and results as PDFs, builds a vector store with chemical-aware chunking, and answers structured queries about trial design, endpoints, and outcomes. Designed for the kind of cross-trial comparison work common in pharmaceutical R&D.

### Molecular Literature RAG
Retrieval-augmented generation over a computational chemistry paper library. Chemical formula-aware parsing, molecular structure embeddings alongside text embeddings, and grounded Q&A with source attribution and BibTeX generation.

## Architecture

```
Query → Planning Agent → Tool Selection
            ↓
  ┌─────────┼─────────┐
  ↓         ↓         ↓
PubChem  Literature  ML Model
Agent    Agent       Agent
  ↓         ↓         ↓
  └─────────┼─────────┘
            ↓
    Synthesis Agent → Report
```

## Stack

LangGraph for orchestration, Claude/Ollama for generation, ChromaDB for vector storage, MACE for molecular predictions, PubChem/Semantic Scholar/CrossRef APIs for data retrieval.
