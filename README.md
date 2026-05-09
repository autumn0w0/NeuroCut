# NeuroCut

NeuroCut is an AI video generation backend for creator-style analysis and scene-based faceless video planning.

The current MVP focuses on Phase 1:

- Save and load reusable JSON style profiles
- Generate a narration plan from a topic and selected style
- Split narration into timed scenes
- Produce image prompts, camera motion, transitions, and metadata
- Store each generation run under `exports/job_*`

Phase 2 will add image generation, voiceover, subtitles, and FFmpeg rendering.

## Run The API

```powershell
pip install -r requirements.txt
uvicorn api.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Main Endpoints

- `GET /health`
- `GET /styles`
- `GET /styles/{style_name}`
- `POST /styles`
- `POST /generate`
- `GET /exports`
- `GET /exports/{job_id}`
- `GET /exports/{job_id}/scenes`
- `GET /exports/{job_id}/script`

## Example Generate Request

```json
{
  "topic": "Your Life as a Medieval Baker",
  "style_name": "oddly_specific_lives",
  "video_minutes": 1,
  "scene_duration": 10
}
```

This creates:

```text
exports/job_YYYYMMDD_HHMMSS/
  script.txt
  script.json
  scenes.json
  metadata.json
  frames/
  audio/
```

## LLM Providers

By default, the app uses a deterministic local fallback so the MVP works without API keys.

Optional `.env` settings:

```text
LLM_PROVIDER=groq
GROQ_API_KEY=...
GROQ_MODEL=llama-3.1-70b-versatile

LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=...
OPENROUTER_MODEL=deepseek/deepseek-chat

LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```
