# GenAI-Optimized Supply Chain & Logistics Tracker

This repository contains a full-stack application that demonstrates a real‑time supply‑chain tracking system powered by *Kafka*, *FastAPI*, *MongoDB*, *LangChain*, and a *React* dashboard.

---

## Features

- **Real‑time transit updates** streamed via Apache Kafka and displayed live on a map.
- **AI extraction pipeline** that parses unstructured logistics emails into structured entities using LangChain with few‑shot prompting and strict JSON schema validation (Pydantic).
- **Async backend** built with FastAPI, Motor (MongoDB driver) and WebSocket/SSE endpoints.
- **Docker compose** setup for MongoDB, Kafka, and Zookeeper.
- **One‑click startup** script (`start.sh`) that brings up the entire stack.

---

## Directory Structure

```text
SupplyChainAITracker/
├─ backend/               # FastAPI server
│   ├─ main.py
│   ├─ config.py
│   ├─ kafka_consumer.py
│   ├─ db.py
│   ├─ ai/
│   │   ├─ langchain_extractor.py
│   │   └─ schemas.py
│   └─ routes/
│       ├─ shipments.py
│       └─ documents.py
├─ frontend/              # React dashboard (Vite + Tailwind)
│   ├─ src/
│   │   ├─ App.jsx
│   │   ├─ api.js
│   │   └─ components/
│   │       ├─ LiveTransitMap.jsx
│   │       └─ ExtractedDataGrid.jsx
│   ├─ package.json
│   └─ index.html
├─ data_simulation/       # Scripts to generate mock data & load test Kafka
│   ├─ generate_unstructured_docs.py
│   └─ simulate_kafka_stream.py
├─ docker-compose.yml
├─ requirements.txt
├─ start.sh                # One‑click startup script
└─ README.md               # This file
Prerequisites
Docker Desktop (or Docker Engine) installed.
Python 3.10+ and Node.js (≥18) for local development.
(Optional) OpenAI API key – set OPENAI_API_KEY in the environment to enable real LLM calls.
 If omitted, the extractor falls back to a deterministic mock implementation.


