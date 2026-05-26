# EngBrain

EngBrain is an AI-powered engineering memory and runbook generator for codebases.

The goal is simple: given a software repository, EngBrain reads the useful files, extracts structure, chunks the content, and prepares the repo for future AI-powered search, onboarding, and runbook generation.

This project is currently in the MVP stage. The first milestone is repo ingestion.

## Why EngBrain?

Engineering knowledge is usually scattered across code, README files, docs, tickets, Slack threads, and old runbooks. New developers often waste time asking repeated questions like:

- How does this project work?
- Where is the main logic?
- How do I add a new feature?
- What files should I be careful with?
- What is the correct runbook for this task?

EngBrain is being built to turn that scattered engineering knowledge into structured, searchable, and eventually AI-assisted answers.

## Current MVP Scope

The current version focuses on repository ingestion.

It can:

- Take a local repository path
- Scan useful source and documentation files
- Ignore junk folders like `.git`, `venv`, `node_modules`, and `__pycache__`
- Skip sensitive files like `.env`
- Read valid text/code files
- Store repositories, files, and chunks in SQLite
- Prepare the data for future embeddings and AI retrieval

## Planned Features

Upcoming features include:

- Codebase Q&A with citations
- Repo architecture summary
- Engineering onboarding guide generation
- Task-specific runbook generation
- Chroma/vector database search
- GitHub repository ingestion
- Simple web UI
- Slack/Jira/Linear integrations later

## Tech Stack

- Python
- SQLAlchemy
- SQLite
- FastAPI planned
- Chroma planned
- LLM/RAG layer planned

## Project Structure

```text
engbrain/
  app/
    database.py
    models.py

    services/
      repo_reader.py
      chunker.py

  scripts/
    ingest_repo.py

  README.md
  requirements.txt
