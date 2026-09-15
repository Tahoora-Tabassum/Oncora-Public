# 🧠 Oncora — AI-Powered RAG Assistant for Cancer Nutrition Research

> **Independent AI/ML Research Project · RAG · Information Retrieval · Evidence-Grounded Generation**

Oncora is an AI-powered research assistant exploring how **Retrieval-Augmented Generation (RAG)** can be used to make cancer-nutrition information easier to query while keeping responses grounded in relevant source material.

The project was independently planned, researched, designed, and developed as an exploration of **retrieval, reranking, evidence handling, reasoning, and source-grounded generation**.

---

## ⚠️ Project Status

**Oncora is currently under active development.**

This repository is **not the complete Oncora codebase**.

The public repository contains selected documentation, supporting scripts, and tests intended to demonstrate the project's architecture, development approach, and engineering work.

The core RAG implementation and certain project assets are intentionally kept **private**. This includes parts of the retrieval, reranking, reasoning, evidence-processing, and generation pipeline, as well as the underlying research data and generated indexes.

As development continues, the public repository may be expanded with additional non-sensitive documentation and supporting material.

---

## 🎯 The Problem

Cancer-nutrition information can be distributed across research papers, reference documents, datasets, and other sources, making it difficult to efficiently locate relevant information and connect evidence to an answer.

Oncora explores a different approach:

**Instead of relying solely on an LLM's internal knowledge, retrieve relevant information first and use that evidence as context for generation.**

The goal is to make the resulting answers more:

* 🔎 **Relevant** — retrieve information related to the user's query
* 📚 **Grounded** — generate responses using retrieved evidence
* 🧩 **Structured** — process information through multiple retrieval and reasoning stages
* 🔗 **Traceable** — retain visibility into the evidence supporting an answer

---

## 🏗️ System Architecture

The overall research pipeline follows this general architecture:

```text
                    SOURCE MATERIAL
                          │
                          ▼
                    Data Processing
                          │
                          ▼
                       Chunking
                          │
                          ▼
                 Semantic Embeddings
                          │
                          ▼
                    Vector Index
                          │
                          ▼
                  Candidate Retrieval
                          │
                          ▼
                    Top-30 Results
                          │
                          ▼
                      Reranking
                          │
                          ▼
                     Top-10 Context
                          │
                          ▼
                  Evidence Processing
                          │
                          ▼
                     LLM Generation
                          │
                          ▼
                  Answer + Sources
```

The architecture is designed around the principle that **retrieval quality and evidence handling are just as important as generation** when building a research-oriented AI system.

---

## 🔬 Current Prototype

The current prototype was developed around a curated collection of cancer-nutrition reference material.

### Current dataset / indexing scale

| Component         | Current Prototype |
| ----------------- | ----------------: |
| Source files      |                 6 |
| Indexed chunks    |               281 |
| Initial retrieval |            Top 30 |
| Reranked context  |            Top 10 |
| Vector search     |             FAISS |
| Embeddings        |            Gemini |
| Generation        |            Gemini |

These figures describe the current research prototype and may change as the system evolves.

---

## 🧠 RAG Pipeline

### 1. Document Processing

Reference material is collected and processed into machine-readable content.

### 2. Chunking

Documents are divided into smaller semantic units so that relevant portions can be retrieved independently.

### 3. Embedding

Text chunks are transformed into vector representations using an embedding model.

### 4. Vector Retrieval

FAISS is used to perform similarity-based retrieval against the indexed chunks.

The initial retrieval stage currently produces a larger candidate set before further processing.

### 5. Reranking

Retrieved candidates are evaluated and reordered to identify the most relevant context for the query.

### 6. Evidence Processing

The system contains additional processing for handling retrieved evidence before generation.

### 7. Response Generation

The selected context is passed to an LLM to generate a response grounded in the retrieved material.

### 8. Source Visibility

The system is designed to preserve visibility into the information used to construct an answer, supporting greater auditability than a purely generative approach.

---

## 🧪 Engineering Focus

Oncora is not intended to be just a basic "chat with documents" implementation.

The project explores several components of an AI retrieval system, including:

* Query understanding
* Query expansion
* Semantic retrieval
* Candidate selection
* Reranking
* Evidence fusion
* Evidence graphs
* Reasoning
* Validation
* Source attribution
* Memory
* Retrieval planning
* Answer generation

Some of these components are intentionally **not included in this public repository**.

---

## 📁 Public Repository Structure

```text
Oncora-Public/
│
├── README.md
├── requirements.txt
│
├── brain/
│   └── AI_Brain.md
│
├── scripts/
│   ├── 01_read_excel.py
│   └── 02_chunk_data.py
│
└── tests/
    ├── test_citation_flow.py
    └── test_reasoning_pipeline.py
```

### `brain/`

Contains documentation describing the conceptual AI architecture and design direction of the system.

### `scripts/`

Contains selected supporting data-processing scripts used during the prototype development.

### `tests/`

Contains tests covering selected aspects of the system, including citation flow and reasoning-related behavior.

### `requirements.txt`

Lists the Python dependencies used by the project.

---

## 🔐 Why Isn't the Entire Implementation Public?

This repository is intentionally a **partial public release**.

The complete implementation contains additional proprietary development work, internal architecture, research assets, and implementation details that are not necessary for demonstrating the project's engineering direction.

Keeping those components private allows the project to remain publicly viewable while protecting the deeper implementation as development continues.

The public repository should therefore be viewed as a **technical portfolio and project documentation layer**, rather than a complete open-source release.

---

## 🛠️ Technology Stack

**Languages**

* Python

**AI / ML**

* Retrieval-Augmented Generation (RAG)
* Large Language Models
* Semantic Embeddings
* Information Retrieval
* Reranking

**Infrastructure / Libraries**

* FAISS
* NumPy
* Data processing utilities

**AI Services**

* Google Gemini

**Testing**

* Python testing tools

---

## 📊 What I Worked On

This project was developed independently, including:

* Project planning and architecture
* Research and information gathering
* Data preparation
* RAG pipeline design
* Retrieval strategy
* Evidence handling
* Experimentation
* Testing
* Debugging
* Iterative system development
* Documentation

The project is part of my broader exploration of **AI/ML engineering, information retrieval, and research-oriented AI systems**.

---

## 🚧 Roadmap

Oncora is still under construction.

Potential future work includes:

* Improving retrieval quality
* Experimenting with additional reranking strategies
* Improving evidence selection
* Better evaluation and benchmarking
* More robust citation validation
* Query planning improvements
* Expanded source coverage
* Improved observability and debugging
* User-facing interface development
* More systematic evaluation datasets

The roadmap may change as the research and implementation evolve.

---

## 📌 Important Note

Oncora is a **research/prototype project**, not a medical diagnostic system.

The project is intended to explore AI-assisted information retrieval and evidence-grounded generation. It should not be used as a substitute for qualified medical advice or professional clinical judgment.

---

## 👩‍💻 About the Project

**Oncora** is an independently developed project by **Tahoora**, a Computer Science graduate currently pursuing an MCA.

The project combines my interests in:

**AI/ML · RAG · Research · Data Processing · Information Retrieval · Evidence-Grounded AI**

---

### Project Status

**🟡 Under Construction · Active Development · Partial Public Release**

> This repository represents a selected public portion of the project. The complete implementation is not currently open source.

---

© 2026 Tahoora. All Rights Reserved.

This repository is published for portfolio and educational review purposes. No permission is granted to copy, modify, redistribute, or commercially use the code without explicit permission.
