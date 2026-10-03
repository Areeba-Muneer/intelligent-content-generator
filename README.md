# Intelligent AI Content Generator

A simple AI-powered web application that generates both text content and a matching image.

## Required Pipeline

User Input
→ Text Generation
→ Content Validation
→ Image Prompt Creation
→ Image Generation
→ Final Output

## Features

- Topic input
- Professional, Casual, Friendly, Educational and Persuasive tones
- Short, Medium and Long content
- Realistic, 3D, Minimal, Cinematic and Illustration visual styles
- Text generation through OpenAI
- Generated-content validation
- Context-aware image prompt generation
- AI image generation
- Pipeline status
- User-friendly errors
- Environment-variable API key
- Modular Python architecture

## Project Structure

```text
intelligent-content-generator/
├── app/
│   ├── main.py
│   ├── models/
│   │   └── schemas.py
│   ├── services/
│   │   ├── text_generator.py
│   │   ├── validator.py
│   │   ├── image_prompt.py
│   │   └── image_generator.py
│   └── utils/
│       └── errors.py
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── generated_images/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 1. Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Configure the API key

Copy `.env.example` to `.env`.

Windows:

```bash
copy .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Then edit `.env`:

```env
OPENAI_API_KEY=your_real_api_key
TEXT_MODEL=gpt-6-luna
IMAGE_MODEL=gpt-image-2
```

Use model IDs that are actually available to your OpenAI API account. If your account uses different/current model IDs, change the two environment variables instead of changing application code.

## 4. Start the server

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## 5. Test

Example:

Topic:
`The future of artificial intelligence in education`

Tone:
`Professional`

Length:
`Medium`

Visual style:
`3D`

Then click **Generate Content**.

## API

### GET /

Loads the web interface.

### GET /health

Checks that the backend is running.

### POST /generate

Accepts:

```json
{
  "topic": "The future of AI in education",
  "tone": "Professional",
  "content_length": "Medium",
  "visual_style": "3D"
}
```

## Security

Never commit `.env` or your API key to GitHub.

The real key belongs in `.env`; `.gitignore` excludes it.

## Assignment Mapping

| Requirement | Implementation |
|---|---|
| Topic | `static/index.html` |
| Tone | `static/index.html` |
| Content Length | `static/index.html` |
| Visual Style | `static/index.html` |
| Text Generation | `services/text_generator.py` |
| Validation | `services/validator.py` |
| Image Prompt | `services/image_prompt.py` |
| Image Generation | `services/image_generator.py` |
| Error Handling | `main.py` + frontend |
| Pipeline Status | `static/script.js` |
| Final Text | Frontend result panel |
| Final Image | Frontend result panel |
| Secure API key | `.env` |

## Important

The frontend pipeline indicators are intentionally lightweight. The backend performs the actual stages in the required order. For a more advanced version, WebSockets or Server-Sent Events can be added for real-time backend progress updates.


## Troubleshooting Text Generation

If the UI says `Failed at text_generation`, open the terminal where Uvicorn is running.
The updated version now returns the actual server error in the browser as well.

Also open:

```text
http://127.0.0.1:8000/health
```

It should show:

```json
{
  "status": "ok",
  "openai_key_configured": true,
  "text_model": "gpt-6-luna",
  "image_model": "gpt-image-2"
}
```

If `openai_key_configured` is `false`, your `.env` is missing/not loaded.

If the error says authentication/401, the API key is invalid.

If it says quota/billing/429, the API project needs available API billing/quota.

If it says model access/404, set `TEXT_MODEL` in `.env` to a model available to your API project.
