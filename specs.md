# Software Specification Document

**Project Name:** Relevantic Recall  
**Version:** 0.1 (Draft)  
**Author:** [Your Name]  
**Date:** [2025-08-29]

---

## 1. Overview

**Relevantic Recall** is a backend service that augments conversational AI applications (e.g., Open WebUI) with **Retrieval-Augmented Generation (RAG)** and **GraphRAG**. It enables long-running chat sessions with contextual awareness by combining:

1. **Traditional RAG (vector similarity search)** – retrieves semantically similar chat messages and responses.
    
2. **GraphRAG (entity and fact reasoning)** – maintains a knowledge graph of entities and relationships, allowing fact-based retrieval and reasoning.
    

The system stores user interactions (messages, transcripts) in PostgreSQL and Neo4j, enabling real-time context retrieval and background fact discovery.

---

## 2. System Architecture

### 2.1 Components

- **Frontend** (e.g., Open WebUI or custom client)
    
    - Sends user messages/queries
        
    - Receives chat completions and streamed facts (WebRTC)
        
- **Backend Service (Python)**
    
    - **API Layer** (REST/GraphQL with OAuth2 auth)
        
    - **Chat Processor**
        
        - Detects message type: **statement vs. question**
            
        - Calls LLM for entity/relation extraction (triplets)
            
    - **Vector Store** (PostgreSQL + pgvector)
        
        - Stores embeddings of user messages and completions
            
    - **Knowledge Graph Store** (Neo4j)
        
        - Stores entity nodes and weighted relationship triplets
            
    - **Entity Dictionary** (PostgreSQL)
        
        - Maps text mentions to disambiguated entity instances
            
    - **Fact Processor (async)**
        
        - Inserts/updates facts in Neo4j
            
        - Resolves conflicting facts, adjusts weights
            
        - Streams updates to frontend via WebRTC
            

### 2.2 Data Flow

1. User sends a message → Backend API receives request
    
2. Embeddings are generated → stored in vector DB
    
3. If **statement**:
    
    - Entities + relationships extracted → graph updated
        
    - Async fact updates streamed via WebRTC
        
4. If **question**:
    
    - Vector similarity search retrieves text chunks
        
    - Entities extracted → GraphDB queried
        
    - Facts streamed asynchronously
        
    - Context (text + facts) assembled → sent to LLM → response returned
        
5. Response embeddings stored in vector DB
    

---

## 3. Data Model

### 3.1 PostgreSQL

- **ChatHistory**
    
    - `id` (UUID, PK)
        
    - `user_id`
        
    - `session_id`
        
    - `message_text`
        
    - `role` (user | assistant)
        
    - `embedding` (vector)
        
    - `source_metadata` (JSONB)
        
    - `timestamp`
        
- **EntityDictionary**
    
    - `id` (UUID, PK)
        
    - `name` (text)
        
    - `canonical_form` (text)
        
    - `entity_type` (person, place, thing, org, event, etc.)
        
    - `user_id` (optional)
        

### 3.2 Neo4j (Graph DB)

- **Nodes:**
    
    - `Entity { id, name, type, metadata }`
        
- **Relationships (limited verb set):**
    
    - `(:Entity)-[:LIKES { weight, user_id, session_id, source, timestamp }]->(:Entity)`
        
    - `(:Entity)-[:KNOWS]->(:Entity)`
        
    - `(:Entity)-[:LOCATED_IN]->(:Entity)`
        
    - …(configurable set of verbs)
        

---

## 4. API Specification

### 4.1 Authentication

- OAuth2 (per-user access control)
    
- Only user’s own chat history is searchable
    

### 4.2 Endpoints

#### `POST /chat`

- **Request:**
    
    ```json
    {
      "session_id": "uuid",
      "user_id": "uuid",
      "message": "John likes Mary.",
      "role": "user"
    }
    ```
    
- **Response (initial):**
    
    ```json
    {
      "status": "processing",
      "llm_response": "pending"
    }
    ```
    
- **Async Streaming (WebRTC events):**
    
    ```json
    {
      "type": "fact_update",
      "entity": "John",
      "relation": "likes",
      "target": "Mary",
      "weight": 1.0
    }
    ```
    

#### `GET /context/:session_id`

- Retrieves most relevant context (chat history + graph facts)
    

#### `POST /entity/resolve`

- Resolves entity mention → canonical form
    

---

## 5. Processing Logic

### 5.1 Statements

- Extract entities + relations → insert into graph
    
- Increment weight if fact already exists
    
- Handle conflicting facts → store both, with weights
    

### 5.2 Questions

- Retrieve:
    
    - Similar chunks from vector DB
        
    - Facts about mentioned entities
        
- Return both as context for LLM
    

### 5.3 Fact Weighting

- Reinforcement: +weight if reiterated
    
- Decay: facts not reaffirmed lose weight over time
    
- Conflicting facts: returned with relative weights
    

---

## 6. Non-Functional Requirements

- **Performance:** Context retrieval < 200ms for vector DB; graph queries may stream async
    
- **Scalability:** Support multi-user, multi-session workloads
    
- **Reliability:** Must handle dropped WebRTC connections gracefully
    
- **Security:** OAuth2 auth; all data scoped to user sessions
    
- **Extensibility:** Future support for multimodal (images/audio links)
    