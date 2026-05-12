# FastAPI AI Starter System

Production-ready FastAPI backend foundation for GenAI, RAG, and Agentic AI systems.

---

# Features

- FastAPI backend
- OpenAI provider abstraction
- streaming response support
- Redis semantic caching
- PostgreSQL integration support
- Docker support
- docker-compose infrastructure
- CI/CD workflows
- pytest validation
- structured logging
- retry/resilience toolkit

---

# Local Setup

## 1. Clone Repository

```bash
git clone <repo-url>
cd fastapi-ai-starter
```

---

## 2. Environment Setup

```bash
cp .env.example .env
```

Update API keys inside `.env`

---

## 3. Install Dependencies

```bash
make install
```

---

## 4. Run Application

```bash
make run
```

Application URL:

```text
http://localhost:8000
```

---

# Docker Deployment

## Build Container

```bash
make build
```

## Start Full Infrastructure

```bash
make compose-up
```

---

# API Validation

## Health Check

```bash
curl http://localhost:8000/health
```

Expected Response:

```json
{
  "status": "healthy",
  "service": "ai-engineering-platform",
  "version": "0.1.0",
  "environment": "development"
}
```

---

## AI Chat Endpoint

```bash
curl -X POST http://localhost:8000/api/v1/ai/chat \
-H "Content-Type: application/json" \
-d '{
  "query": "Explain RAG architecture"
}'
```

Expected Response:

```json
{
  "success": true,
  "response": "Processed query: Explain RAG architecture",
  "latency_ms": 12.4,
  "provider": "foundation-template"
}
```

---

# Test Validation

Run tests:

```bash
make test
```

Run linting:

```bash
make lint
```

Run type checks:

```bash
make typecheck
```

---

# Infrastructure Stack

| Component | Purpose |
|---|---|
| FastAPI | API layer |
| PostgreSQL | Structured storage |
| Redis | Semantic cache |
| Docker | Containerization |
| GitHub Actions | CI/CD |
| OpenAI | LLM inference |

---

# Future Extensions

- JWT authentication
- LangGraph integration
- RAG pipelines
- vector databases
- observability dashboards
- streaming UI
- agent orchestration
- MCP integration
