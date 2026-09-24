# StudyScript — AI Handwritten Study Notes Generator

An original MVP that converts a topic, syllabus, PDF syllabus, or YouTube lecture transcript into validated structured notes, hand-rendered A4 pages, and a downloadable PDF. The built-in deterministic note provider keeps the full flow usable locally without an API key; set `GEMINI_API_KEY` to use Gemini when available.

## Run

```bash
cp .env.example .env
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
cd backend && uvicorn main:app --reload --port 8000
```

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. Optional frontend configuration: `VITE_API_URL=http://localhost:8000`.

## Environment

- `GEMINI_API_KEY`: Optional. Enables Gemini structured-note generation. If unset or provider fails, the safe local educational template is used.
- `FRONTEND_URL`, `BACKEND_URL`: Deployment configuration values.

## API

- `GET /api/health`
- `POST /api/generate/topic` with `{topic, instruction, include_diagrams, include_examples, exam_oriented}`
- `POST /api/generate/syllabus`, `POST /api/generate/syllabus-pdf`, `POST /api/generate/youtube`
- `POST /api/parse/syllabus`, `POST /api/youtube/transcript`
- `GET /api/generation/{id}`, `/api/generation/{id}/pages`, `/api/generation/{id}/pdf`

Interactive OpenAPI documentation is at `/docs` while the backend is running.

## Tests

```bash
cd backend && pytest ../tests -q
cd frontend && npm run build
```

## Known limitations and next steps

This MVP uses PIL text rendering with deterministic baseline variation, rather than per-glyph vector outlines, and diagrams currently use a hand-drawn flowchart vocabulary. Syllabus and YouTube endpoints are implemented but the current frontend treats non-topic modes as an MVP demo. Next steps: connect all mode forms, add robust table/math SVG layout, provider response repair telemetry, and a queue/worker for deployment scale.
