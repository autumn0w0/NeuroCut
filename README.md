# NeuroCut

NeuroCut is an AI video generation backend for faceless storytelling videos.

The current generation flow is simple:

- User enters `title`
- User enters `base_idea`
- Every video is fixed at 8 minutes
- The system writes a second-person cinematic script
- The script is split sentence-by-sentence into scenes
- Each sentence gets a matching image prompt
- The number of prompts equals the number of images
- Image prompts are saved in 4 parts
- Gemini TTS creates narration with the `Achird` voice
- Scene images are generated as PNGs when an image provider is available

## Run The API

```powershell
pip install -r requirements.txt
uvicorn api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Generate Request

```json
{
  "title": "Your Life As a NEET Aspirant in Kota",
  "base_idea": "You just completed 10th and moved to Kota for NEET prep. You have a hard time adjusting to food and schedule. You are having money problems and even after all the hardships you still cannot clear NEET in the first attempt and take a drop."
}
```

## Output

```text
exports/job_YYYYMMDD_HHMMSS/
  script.txt
  script.json
  scenes.json
  image_prompts_part_1.json
  image_prompts_part_2.json
  image_prompts_part_3.json
  image_prompts_part_4.json
  metadata.json
  frames/
  audio/
    voiceover.wav
    subtitles.srt
```

## Gemini TTS

Set one of these in `.env`:

```text
GOOGLE_API_KEY=...
```

or:

```text
GEMINI_API_KEY=...
```

Optional:

```text
GEMINI_TTS_MODEL=gemini-2.5-flash-preview-tts
GEMINI_TTS_VOICE=Achird
```

## Image Providers

Default:

```text
IMAGE_PROVIDER=pollinations
IMAGE_WIDTH=1280
IMAGE_HEIGHT=720
```

Local Stable Diffusion with Automatic1111:

```text
IMAGE_PROVIDER=automatic1111
AUTOMATIC1111_BASE_URL=http://127.0.0.1:7860
```

The pipeline generates one image per script sentence.
