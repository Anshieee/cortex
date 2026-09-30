# Cortex

A work-in-progress second-brain project. The code currently on `main` includes a knowledge-graph extraction API and a React/Tauri desktop client scaffold.

## Current implementation

- FastAPI exposes `POST /extract` for text input and `GET /health`.
- Gemini 2.5 Flash and Instructor extract nodes and relationships into Pydantic schemas.
- Relationships with a model-reported confidence score below 0.85 are removed.
- Edges that reference missing nodes are removed.
- `cortex-client/` contains the React, TypeScript, and Tauri client scaffold.

The confidence threshold is a filtering rule, not a measured accuracy guarantee. The checked `main` branch does not yet provide a complete retrieval-and-answering flow or a connected desktop UI.

## Repository layout

- `cortex-ai/`: extraction API, schemas, model client, and example/mock data.
- `cortex-client/`: desktop client scaffold.

## Development

The backend needs Python dependencies from `cortex-ai/requirements.txt` and a Gemini API credential configured for the Google Gen AI SDK. The client uses Node.js/npm; desktop development also needs Rust and the Tauri prerequisites for your OS.

A tested, end-to-end setup guide and demo will be added after the backend and client are connected. Do not commit API credentials.

## Status

This is a temporary README. Setup verification, retrieval functionality, demo footage, evaluation results, and contributor details still need documentation. No performance or retrieval-quality benchmark is claimed here.
