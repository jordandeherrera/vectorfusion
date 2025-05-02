# Open Converged Index Project (Placeholder Name)

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Build Status](https://img.shields.io/badge/Build-Pending-lightgrey)](...) [![Documentation Status](https://img.shields.io/badge/Docs-WIP-orange)](...) An open-source initiative to build a high-performance data platform featuring tightly integrated vector search and metadata/keyword filtering, inspired by architectures like Rockset's Converged Index™.

---

## Table of Contents

- [Overview](#overview)
- [Core Principle](#core-principle-tight-integration--optimization)
- [Key Requirements](#key-requirements)
- [Architecture](#architecture)
  - [Indexing Layer](#1-indexing-layer)
  - [Query Engine](#2-query-engine)
  - [Storage Layer](#3-storage-layer)
  - [Ingestion Layer](#4-ingestion-layer)
  - [API Layer](#5-api-layer)
- [Technology Stack](#technology-stack)
- [Example Query Workflow](#example-query-workflow)
- [Performance Goals](#performance-goals)
- [Development Roadmap](#development-roadmap)
- [Getting Started (Future)](#getting-started-future)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Modern applications increasingly need to search through vast datasets using a combination of semantic similarity (via vector embeddings) and traditional structured or keyword filters. Performing these "hybrid" queries efficiently at scale is challenging. Existing solutions often involve separate vector databases and traditional databases, leading to data duplication, synchronization complexities, and potentially high latencies.

This project aims to create an open-source platform that natively supports hybrid search within a single, optimized system. By building upon proven open-source components and focusing on deep integration, we aim to provide a powerful, scalable, and performant alternative without proprietary lock-in.

## Core Principle: Tight Integration & Optimization

The fundamental goal is to achieve performance comparable to systems like Rockset's Converged Index. This requires seamless integration of vector indexing (for similarity search) with metadata/keyword indexing (for filtering). A sophisticated query optimizer that understands both index types is crucial to minimize expensive vector operations and achieve low-latency (sub-second, aiming for tens of milliseconds) hybrid queries.

## Key Requirements

-   **Open Source**: Built entirely with or upon open-source technologies (Apache 2.0 License).
-   **Converged Index**: A unified indexing system handling vectors, keywords, and structured metadata without data duplication or complex sync.
-   **High Performance**: Target low-latency queries (tens of milliseconds) for combined vector and filter operations.
-   **Scalability**: Designed for horizontal scaling to handle billions of vectors and terabytes/petabytes of data.
-   **Real-time Ingestion**: Capable of indexing new data rapidly for near real-time query availability.
-   **User-Friendly Interface**: Offer a familiar API, primarily SQL-like with vector extensions, for ease of adoption.

## Architecture

The proposed architecture is built on several key pillars:

### 1. Indexing Layer

-   **Vector Indexing**: Utilizes state-of-the-art Approximate Nearest Neighbor (ANN) algorithms like HNSW (via `hnswlib` or `Faiss`). Key challenge: Extending these to be metadata-aware for efficient filtering *during* the search process.
-   **Metadata/Keyword Indexing**:
    -   **Structured Data**: Leverages columnar formats (`Apache Arrow`) and potentially bitmap indexes for fast filtering.
    -   **Text Search**: Employs inverted indexes (`Apache Lucene`).
-   **Integration Strategy**: Supports both pre-filtering (filter metadata first, then vector search on the subset) and metadata-aware ANN search (check filters during ANN graph traversal) to minimize vector distance calculations.

### 2. Query Engine

-   **Planner/Optimizer**: A cost-aware planner that intelligently reorders operations, prioritizing filters before expensive vector searches (predicate pushdown).
-   **Execution**: Optimized execution using SIMD instructions (e.g., AVX2) for distance calculations and parallel processing.
-   **API**: A SQL-like interface with vector extensions (e.g., `COSINE_SIMILARITY`).

### 3. Storage Layer

-   Combines row-oriented (for full record retrieval) and column-oriented (for filtering) storage approaches.
-   Optimized for in-memory ANN indexes with robust disk-based persistence using memory-mapped files and storage engines like `RocksDB`.

### 4. Ingestion Layer

-   Designed for real-time updates, potentially using buffering, delta indexes, or Log-Structured Merge-tree (LSM) inspired approaches adapted for concurrent vector/metadata updates. Addresses the challenge of updating static ANN structures.

### 5. API Layer

-   Primary interface via **SQL** with vector function extensions.
-   Secondary **REST/gRPC API** for broader integration flexibility.

## Technology Stack

This project intends to leverage and integrate the following battle-tested open-source components:

-   **Vector Indexing**: Faiss / hnswlib
-   **Text Search**: Apache Lucene
-   **In-Memory Columnar Data**: Apache Arrow
-   **Persistent Storage**: RocksDB

The core innovation lies in the tight integration of these components and the development of a custom, convergence-aware query engine.

## Example Query Workflow

Consider a hybrid query:

```sql
SELECT item_id, name
FROM products
WHERE category = 'electronics' AND price < 100.00
ORDER BY COSINE_SIMILARITY(embedding, :query_vector) DESC
LIMIT 10;


The query engine would likely execute this as follows:
Metadata Filtering: Use the Lucene/Arrow indexes to quickly identify all products where category = 'electronics' AND price < 100.00. This drastically reduces the candidate set (e.g., from millions to thousands).
Vector Search: Perform an ANN (HNSW) search only on the filtered subset of product embeddings against the :query_vector.
Ranking & Retrieval: Retrieve the top 10 results based on cosine similarity.
This filter-then-search approach is key to achieving high performance by minimizing costly vector operations.
Performance Goals
Low Latency: Aim for P99 latencies in the tens of milliseconds for typical hybrid queries.
High Throughput: Support high concurrent query loads.
Efficient Resource Usage: Optimize memory (via techniques like Product Quantization) and CPU (via SIMD, parallelism) usage.
Scalability: Linear scaling of ingestion and query performance with added nodes.
Development Roadmap
Development is planned in iterative phases:
Phase 1: Build an in-memory prototype demonstrating core vector search integrated with basic metadata pre-filtering. Establish baseline performance benchmarks.
Phase 2: Implement disk-based persistence (RocksDB integration) and develop the real-time ingestion pipeline. Refine the query optimizer.
Phase 3: Focus on horizontal scalability, advanced query optimization (e.g., metadata-aware HNSW), fault tolerance, and API hardening. Build community tooling and documentation.
Getting Started (Future)
(This section is a placeholder until code is available)
Once the initial prototype is available:

Bash


# Clone the repository (link TBD)
git clone [https://github.com/your-org/open-converged-index.git](https://github.com/your-org/open-converged-index.git)
cd open-converged-index

# Build instructions (TBD)
./build.sh # Example

# Run instructions (TBD)
./server # Example


Contributing
We welcome contributions from the community! If you're interested in helping build the next generation of open-source hybrid search, please consider:
Reviewing the architecture and providing feedback.
Contributing code, particularly in areas like:
Integrating Faiss/Lucene/Arrow/RocksDB.
Developing the query planner and optimizer.
Implementing metadata-aware ANN algorithms.
Building robust ingestion and storage layers.
Creating benchmarks and documentation.
Opening issues for bugs or feature requests.
Please adhere to the project's code of conduct and contribution guidelines (to be created). We aim to build an open, collaborative community around clear documentation and transparent benchmarks.
License
This project is licensed under the Apache License 2.0. See the https://www.google.com/search?q=LICENSE file for details.



**Key changes and considerations in this README:**

1.  **Project Name:** Used a placeholder `Open Converged Index Project`. You'll want to choose a real name.
2.  **Badges:** Added standard placeholder badges for License, Build Status, and Docs.
3.  **Table of Contents:** Included for easy navigation.
4.  **Clearer Sections:** Organized the information into standard README sections like Overview, Architecture, Technology Stack, Roadmap, Contributing, etc.
5.  **Motivation:** Clearly stated the problem being solved (efficient hybrid search, open-source alternative).
6.  **Audience:** Written for potential users and contributors, explaining the *what*, *why*, and *how*.
7.  **Conciseness:** Summarized the detailed architecture while retaining the key concepts.
8.  **Example Query:** Kept the concrete example as it's very illustrative.
9.  **Call to Action:** Included a "Contributing" section to encourage community involvement.
10. **Placeholders:** Marked areas like build instructions and repository links as TBD.
11. **License File:** Assumes a `LICENSE` file will exist in the repository.
